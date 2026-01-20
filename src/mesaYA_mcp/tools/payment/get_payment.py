"""Get payment status tool."""

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


class GetPaymentDto(BaseModel):
    """DTO for getting payment details."""

    payment_id: str = Field(..., description="The payment ID to look up")


# Payment microservice URL from environment
PAYMENT_MS_URL = os.getenv("PAYMENT_MS_URL", "http://localhost:8003")


@mcp.tool()
@require_access(AccessLevel.USER)
async def get_payment_status(dto: GetPaymentDto) -> str:
    """Get the status of a payment. Requires USER access.

    Retrieves payment details from the Payment Microservice.

    Args:
        dto: Payment ID to look up.

    Returns:
        Payment status and details in TOON format.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info(
        "Getting payment status",
        context="get_payment",
        payment_id=dto.payment_id,
    )

    try:
        # Call Payment Microservice
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{PAYMENT_MS_URL}/api/v1/payments/{dto.payment_id}"
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "Payment retrieved successfully",
                    context="get_payment",
                    payment_id=dto.payment_id,
                    status=data.get("status"),
                )
                return adapter.map_to_toon(
                    data={
                        "payment_id": data.get("id"),
                        "status": data.get("status"),
                        "amount": data.get("amount"),
                        "currency": data.get("currency"),
                        "description": data.get("description"),
                        "created_at": data.get("created_at"),
                        "metadata": data.get("metadata"),
                    },
                    entity_type="payment",
                    operation="retrieve",
                )
            elif response.status_code == 404:
                logger.warning(
                    "Payment not found",
                    context="get_payment",
                    payment_id=dto.payment_id,
                )
                return adapter.map_not_found("payment", dto.payment_id)
            else:
                error_detail = response.json().get("detail", "Unknown error")
                logger.error(
                    "Failed to get payment",
                    context="get_payment",
                    status_code=response.status_code,
                    error=error_detail,
                )
                return adapter.map_error(
                    message=f"Failed to retrieve payment: {error_detail}",
                    entity_type="payment",
                    operation="retrieve",
                )

    except httpx.TimeoutException:
        logger.error("Payment service timeout", context="get_payment")
        return adapter.map_error(
            message="Payment service is not responding. Please try again later.",
            entity_type="payment",
            operation="retrieve",
        )
    except httpx.ConnectError:
        logger.error("Cannot connect to payment service", context="get_payment")
        return adapter.map_error(
            message="Cannot connect to payment service. Please try again later.",
            entity_type="payment",
            operation="retrieve",
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting payment",
            context="get_payment",
            error=str(e),
        )
        return adapter.map_error(
            message=f"An unexpected error occurred: {str(e)}",
            entity_type="payment",
            operation="retrieve",
        )


__all__ = ["get_payment_status"]
