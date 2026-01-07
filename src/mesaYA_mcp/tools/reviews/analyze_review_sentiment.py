"""Analyze Review Sentiment Tool.

Uses LLM (Gemini/OpenAI) to classify review sentiment as
POSITIVE, NEUTRAL, or NEGATIVE. Extracts keywords and confidence score.

This tool is designed to be called asynchronously after review creation.
"""

from mesaYA_mcp.server import mcp
from mesaYA_mcp.shared.core import get_logger, get_settings
from mesaYA_mcp.shared.infrastructure.adapters.toon_response_adapter import (
    get_response_adapter,
)

# LangChain imports for LLM integration
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class SentimentAnalysisInput(BaseModel):
    """Input for sentiment analysis."""

    text: str = Field(description="The review text to analyze")
    rating: int = Field(
        default=3, ge=1, le=5, description="The numeric rating (1-5) given by the user"
    )


class SentimentAnalysisResult(BaseModel):
    """Output schema for sentiment analysis."""

    sentiment: str = Field(
        description="Sentiment classification: POSITIVE, NEUTRAL, or NEGATIVE"
    )
    confidence: float = Field(
        description="Confidence score between 0 and 1", ge=0, le=1
    )
    keywords: list[str] = Field(
        description="Key phrases or words that influenced the classification"
    )
    summary: str = Field(description="Brief summary of the review sentiment")


# System prompt for sentiment analysis
SENTIMENT_ANALYSIS_PROMPT = """You are an expert sentiment analyzer for restaurant reviews.

Analyze the following restaurant review and classify its sentiment.

CLASSIFICATION RULES:
- POSITIVE: The review expresses satisfaction, happiness, or praise. Rating 4-5 usually supports this.
- NEGATIVE: The review expresses dissatisfaction, complaints, or criticism. Rating 1-2 usually supports this.
- NEUTRAL: The review is mixed, balanced, or doesn't express strong emotion. Rating 3 is often neutral.

Consider both the text content AND the numeric rating.
Extract keywords that best represent the sentiment (e.g., "great service", "cold food", "slow waiter").

REVIEW TEXT: {text}
RATING: {rating}/5

Respond in JSON format with:
- sentiment: "POSITIVE" | "NEUTRAL" | "NEGATIVE"
- confidence: float between 0 and 1
- keywords: list of 2-5 key phrases
- summary: one sentence explaining the classification
"""


def _get_llm():
    """Get LLM instance based on available API keys."""
    settings = get_settings()

    # Try Gemini first (free tier available)
    gemini_key = getattr(settings, "gemini_api_key", None)
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=gemini_key,
                temperature=0.1,
            )
        except ImportError:
            pass

    # Fall back to OpenAI
    openai_key = getattr(settings, "openai_api_key", None)
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model="gpt-4o-mini",
                api_key=openai_key,
                temperature=0.1,
            )
        except ImportError:
            pass

    # Final fallback: Groq (usually available)
    groq_key = getattr(settings, "groq_api_key", None)
    if groq_key:
        try:
            from langchain_groq import ChatGroq

            return ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=groq_key,
                temperature=0.1,
            )
        except ImportError:
            pass

    return None


@mcp.tool()
async def analyze_review_sentiment(dto: SentimentAnalysisInput) -> str:
    """Analyze restaurant review sentiment using AI.

    Args:
        text: The review text to analyze
        rating: Optional numeric rating (1-5)

    Returns:
        Sentiment classification (POSITIVE/NEUTRAL/NEGATIVE),
        confidence score, keywords, and summary.
    """
    logger = get_logger()
    adapter = get_response_adapter()

    logger.info(
        "Analyzing review sentiment",
        context="analyze_review_sentiment",
        text_length=len(dto.text),
        rating=dto.rating,
    )

    # Validate input
    if not dto.text or len(dto.text.strip()) < 3:
        return adapter.map_error(
            message="Review text is too short to analyze",
            entity_type="review_sentiment",
            operation="analyze",
        )

    # Get LLM
    llm = _get_llm()
    if not llm:
        # Fallback to rule-based analysis if no LLM available
        logger.warning(
            "No LLM available, using rule-based sentiment analysis",
            context="analyze_review_sentiment",
        )
        return _rule_based_analysis(dto, adapter)

    try:
        # Build the chain
        prompt = ChatPromptTemplate.from_template(SENTIMENT_ANALYSIS_PROMPT)
        parser = JsonOutputParser(pydantic_object=SentimentAnalysisResult)

        chain = prompt | llm | parser

        # Execute analysis
        result = await chain.ainvoke({"text": dto.text, "rating": dto.rating})

        logger.info(
            "Sentiment analysis completed",
            context="analyze_review_sentiment",
            sentiment=result.get("sentiment"),
            confidence=result.get("confidence"),
        )

        return adapter.map_success(
            data={
                "sentiment": result.get("sentiment", "NEUTRAL"),
                "confidence": result.get("confidence", 0.5),
                "keywords": result.get("keywords", []),
                "summary": result.get("summary", ""),
                "analyzed_at": "now",
            },
            entity_type="review_sentiment",
            operation="analyze",
        )

    except Exception as e:
        logger.error(
            "Sentiment analysis failed",
            error=str(e),
            context="analyze_review_sentiment",
        )
        # Fallback to rule-based
        return _rule_based_analysis(dto, adapter)


def _rule_based_analysis(dto: SentimentAnalysisInput, adapter) -> str:
    """Simple rule-based sentiment analysis as fallback."""
    positive_words = {
        "great",
        "excellent",
        "amazing",
        "wonderful",
        "fantastic",
        "delicious",
        "love",
        "best",
        "perfect",
        "recommend",
        "friendly",
        "fresh",
        "quick",
        "clean",
    }
    negative_words = {
        "bad",
        "terrible",
        "awful",
        "horrible",
        "worst",
        "disgusting",
        "hate",
        "slow",
        "cold",
        "rude",
        "dirty",
        "expensive",
        "disappointing",
        "never",
    }

    text_lower = dto.text.lower()
    words = set(text_lower.split())

    pos_count = len(words & positive_words)
    neg_count = len(words & negative_words)

    # Combine with rating
    if dto.rating >= 4 or (pos_count > neg_count and dto.rating >= 3):
        sentiment = "POSITIVE"
        confidence = 0.7 if dto.rating >= 4 else 0.5
    elif dto.rating <= 2 or (neg_count > pos_count and dto.rating <= 3):
        sentiment = "NEGATIVE"
        confidence = 0.7 if dto.rating <= 2 else 0.5
    else:
        sentiment = "NEUTRAL"
        confidence = 0.4

    keywords = list((words & positive_words) | (words & negative_words))[:5]

    return adapter.map_success(
        data={
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": keywords,
            "summary": f"Rule-based analysis based on rating ({dto.rating}/5) and keywords",
            "analyzed_at": "now",
            "method": "rule_based",
        },
        entity_type="review_sentiment",
        operation="analyze",
    )
