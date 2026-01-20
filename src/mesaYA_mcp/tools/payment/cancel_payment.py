"""Cancel payment tool."""

import os
from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger
from mesaYA_mcp.shared.domain.access_level import AccessLevel
from mesaYA_mcp.shared.application.require_access_decorator import require_access
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)
from pydantic import BaseModel, Field
import httpx


class CancelPaymentDto(BaseModel):
    """DTO for cancelling a payment."""

    payment_id: str = Field(..., description="The payment ID to cancel")
    reason: str | None = Field(default=None, description="Reason for cancellation")


# Payment microservice URL from environment
PAYMENT_MS_URL = os.getenv("PAYMENT_MS_URL", "http://localhost:8003")


@mcp.tool()
@require_access(AccessLevel.OWNER)
async def cancel_payment(dto: CancelPaymentDto) -> str:
    """Cancel a pending payment. Requires OWNER access.

    Cancels a payment that hasn't been completed yet.
    For completed payments, use refund instead.

    Args:
        dto: Payment ID to cancel and optional reason.

    Returns:
        Cancellation result in TOON format.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info(
        "Cancelling payment",
        context="cancel_payment",
        payment_id=dto.payment_id,
        reason=dto.reason,
    )

    try:
        # Call Payment Microservice
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{PAYMENT_MS_URL}/api/v1/payments/{dto.payment_id}/cancel",
                json={"reason": dto.reason} if dto.reason else {},
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "Payment cancelled successfully",
                    context="cancel_payment",
                    payment_id=dto.payment_id,
                )
                return adapter.map_to_toon(
                    data={
                        "payment_id": dto.payment_id,
                        "status": "cancelled",
                        "message": "Payment has been cancelled successfully.",
                    },
                    entity_type="payment",
                    operation="cancel",
                )
            elif response.status_code == 404:
                logger.warning(
                    "Payment not found",
                    context="cancel_payment",
                    payment_id=dto.payment_id,
                )
                return adapter.map_not_found("payment", dto.payment_id)
            elif response.status_code == 400:
                error_detail = response.json().get("detail", "Cannot cancel this payment")
                logger.warning(
                    "Cannot cancel payment",
                    context="cancel_payment",
                    payment_id=dto.payment_id,
                    error=error_detail,
                )
                return adapter.map_error(
                    message=f"Cannot cancel payment: {error_detail}",
                    entity_type="payment",
                    operation="cancel",
                )
            else:
                error_detail = response.json().get("detail", "Unknown error")
                logger.error(
                    "Failed to cancel payment",
                    context="cancel_payment",
                    status_code=response.status_code,
                    error=error_detail,
                )
                return adapter.map_error(
                    message=f"Failed to cancel payment: {error_detail}",
                    entity_type="payment",
                    operation="cancel",
                )

    except httpx.TimeoutException:
        logger.error("Payment service timeout", context="cancel_payment")
        return adapter.map_error(
            message="Payment service is not responding. Please try again later.",
            entity_type="payment",
            operation="cancel",
        )
    except httpx.ConnectError:
        logger.error("Cannot connect to payment service", context="cancel_payment")
        return adapter.map_error(
            message="Cannot connect to payment service. Please try again later.",
            entity_type="payment",
            operation="cancel",
        )
    except Exception as e:
        logger.error(
            "Unexpected error cancelling payment",
            context="cancel_payment",
            error=str(e),
        )
        return adapter.map_error(
            message=f"An unexpected error occurred: {str(e)}",
            entity_type="payment",
            operation="cancel",
        )


__all__ = ["cancel_payment"]
