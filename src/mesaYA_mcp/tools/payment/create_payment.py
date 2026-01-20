"""Create payment tool.

Note: MCP tools can call the Payment MS directly since they run on the server side.
The frontend uses the API Gateway (mesa-ya-res) for all payment operations.
"""

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


class CreatePaymentDto(BaseModel):
    """DTO for creating a payment."""

    reservation_id: str = Field(..., description="The reservation ID to pay for")
    amount: float = Field(..., description="Amount to charge", gt=0)
    currency: str = Field(default="USD", description="Currency code (e.g., USD, EUR)")
    description: str | None = Field(default=None, description="Payment description")


# Payment microservice URL - MCP calls directly (server-to-server)
PAYMENT_MS_URL = os.getenv("PAYMENT_MS_URL", "http://localhost:8003")


@mcp.tool()
@require_access(AccessLevel.USER)
async def create_payment_for_reservation(dto: CreatePaymentDto) -> str:
    """Create a payment for a reservation. Requires USER access.

    Creates a checkout session in the Payment Microservice.
    Returns the payment ID and checkout URL for the user to complete payment.

    Args:
        dto: Payment details (reservation_id, amount, currency, description).

    Returns:
        Payment details in TOON format including checkout URL.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info(
        "Creating payment for reservation",
        context="create_payment",
        reservation_id=dto.reservation_id,
        amount=dto.amount,
        currency=dto.currency,
    )

    try:
        # Call Payment Microservice
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{PAYMENT_MS_URL}/api/v1/payments",
                json={
                    "amount": dto.amount,
                    "currency": dto.currency,
                    "description": dto.description or f"Payment for reservation {dto.reservation_id}",
                    "metadata": {
                        "reservation_id": dto.reservation_id,
                        "type": "reservation",
                    },
                },
            )

            if response.status_code == 201:
                data = response.json()
                logger.info(
                    "Payment created successfully",
                    context="create_payment",
                    payment_id=data.get("payment_id"),
                )
                return adapter.map_to_toon(
                    data={
                        "payment_id": data.get("payment_id"),
                        "status": data.get("status"),
                        "amount": data.get("amount"),
                        "currency": data.get("currency"),
                        "checkout_url": data.get("checkout_url"),
                        "message": "Payment created. Use the checkout_url to complete payment.",
                    },
                    entity_type="payment",
                    operation="create",
                )
            else:
                error_detail = response.json().get("detail", "Unknown error")
                logger.error(
                    "Failed to create payment",
                    context="create_payment",
                    status_code=response.status_code,
                    error=error_detail,
                )
                return adapter.map_error(
                    message=f"Payment creation failed: {error_detail}",
                    entity_type="payment",
                    operation="create",
                )

    except httpx.TimeoutException:
        logger.error("Payment service timeout", context="create_payment")
        return adapter.map_error(
            message="Payment service is not responding. Please try again later.",
            entity_type="payment",
            operation="create",
        )
    except httpx.ConnectError:
        logger.error("Cannot connect to payment service", context="create_payment")
        return adapter.map_error(
            message="Cannot connect to payment service. Please try again later.",
            entity_type="payment",
            operation="create",
        )
    except Exception as e:
        logger.error(
            "Unexpected error creating payment",
            context="create_payment",
            error=str(e),
        )
        return adapter.map_error(
            message=f"An unexpected error occurred: {str(e)}",
            entity_type="payment",
            operation="create",
        )


__all__ = ["create_payment_for_reservation"]
