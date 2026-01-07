"""Analyze Menu Image Tool.

Uses vision models (Gemini Pro Vision / GPT-4o) to:
- Extract text from menu images (OCR)
- Identify dishes and their descriptions
- Detect prices
- Describe food photos

Supports images from Supabase Storage URLs or base64 encoded data.
"""

import base64
import httpx
from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_settings
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)

from pydantic import BaseModel, Field


class ImageAnalysisInput(BaseModel):
    """Input for image analysis."""

    image_url: str = Field(
        description="URL of the image to analyze (Supabase Storage or public URL)"
    )
    analysis_type: str = Field(
        default="menu",
        description="Type of analysis: 'menu' for OCR/dish extraction, 'food' for food description",
    )
    language: str = Field(
        default="es",
        description="Expected language of the text: 'es' for Spanish, 'en' for English",
    )


# Prompts for different analysis types
MENU_ANALYSIS_PROMPT = """Analyze this restaurant menu image and extract:

1. **Dishes**: List each dish name you can read
2. **Prices**: Extract prices if visible (format: dish -> price)
3. **Categories**: Identify menu sections (appetizers, mains, desserts, drinks)
4. **Special items**: Note any highlighted or featured items

If text is partially visible or unclear, indicate with [unclear].
Respond in {language}.

Format your response as a structured list with clear sections."""

FOOD_ANALYSIS_PROMPT = """Describe this food/dish image:

1. **Dish identification**: What dish or food is shown?
2. **Ingredients visible**: What ingredients can you identify?
3. **Presentation**: Describe how the food is presented
4. **Portion size**: Estimate (small, medium, large)
5. **Cuisine type**: What type of cuisine does this appear to be?

Respond in {language}."""


async def _download_image(url: str) -> bytes | None:
    """Download image from URL and return bytes."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.content
            return None
    except Exception:
        return None


def _get_vision_model():
    """Get vision-capable LLM based on available API keys."""
    settings = get_settings()

    # Try Gemini Pro Vision first (recommended - free tier)
    gemini_key = getattr(settings, "gemini_api_key", None)
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",  # Vision capable
                google_api_key=gemini_key,
                temperature=0.2,
            ), "gemini"
        except ImportError:
            pass

    # Fall back to OpenAI GPT-4o (vision capable)
    openai_key = getattr(settings, "openai_api_key", None)
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model="gpt-4o",  # Vision capable
                api_key=openai_key,
                temperature=0.2,
            ), "openai"
        except ImportError:
            pass

    return None, None


@mcp.tool()
async def analyze_menu_image(dto: ImageAnalysisInput) -> str:
    """Analyze a menu or food image using AI vision models.

    Args:
        image_url: URL of the image (Supabase Storage or public)
        analysis_type: 'menu' for OCR/extraction, 'food' for description
        language: 'es' for Spanish, 'en' for English

    Returns:
        Extracted text, dishes, prices, or food description.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info(
        "Analyzing image",
        context="analyze_menu_image",
        url=dto.image_url[:50] + "...",
        analysis_type=dto.analysis_type,
    )

    # Validate URL
    if not dto.image_url or not dto.image_url.startswith(("http://", "https://")):
        return adapter.map_error(
            message="Invalid image URL. Must be http:// or https://",
            entity_type="image_analysis",
            operation="analyze",
        )

    # Get vision model
    llm, provider = _get_vision_model()
    if not llm:
        return adapter.map_error(
            message="No vision model available. Configure GEMINI_API_KEY or OPENAI_API_KEY",
            entity_type="image_analysis",
            operation="analyze",
        )

    try:
        # Download image
        image_bytes = await _download_image(dto.image_url)
        if not image_bytes:
            return adapter.map_error(
                message="Could not download image from URL",
                entity_type="image_analysis",
                operation="analyze",
            )

        # Convert to base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Determine MIME type from URL or default to jpeg
        if ".png" in dto.image_url.lower():
            mime_type = "image/png"
        elif ".gif" in dto.image_url.lower():
            mime_type = "image/gif"
        elif ".webp" in dto.image_url.lower():
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"

        # Select prompt based on analysis type
        language_name = "Spanish" if dto.language == "es" else "English"
        if dto.analysis_type == "food":
            prompt_text = FOOD_ANALYSIS_PROMPT.format(language=language_name)
        else:
            prompt_text = MENU_ANALYSIS_PROMPT.format(language=language_name)

        # Build message with image (LangChain multimodal format)
        from langchain_core.messages import HumanMessage

        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt_text},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{image_base64}"},
                },
            ]
        )

        # Execute vision analysis
        response = await llm.ainvoke([message])

        logger.info(
            "Image analysis completed",
            context="analyze_menu_image",
            provider=provider,
        )

        return adapter.map_success(
            data={
                "analysis": response.content,
                "analysis_type": dto.analysis_type,
                "language": dto.language,
                "provider": provider,
                "image_url": dto.image_url,
            },
            entity_type="image_analysis",
            operation="analyze",
        )

    except Exception as e:
        logger.error(
            "Image analysis failed",
            error=str(e),
            context="analyze_menu_image",
        )
        return adapter.map_error(
            message=f"Image analysis failed: {str(e)}",
            entity_type="image_analysis",
            operation="analyze",
        )
