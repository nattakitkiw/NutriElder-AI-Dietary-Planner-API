"""
API v1 endpoint definitions for NutriElder AI Dietary Planner.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ErrorResponse,
    GeneratePlanResponse,
    UserProfile,
)
from app.services.openai_service import generate_meal_plan

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Meal Plan"])


@router.post(
    "/generate-plan",
    response_model=GeneratePlanResponse,
    summary="Generate a 7-day meal plan",
    description=(
        "Accepts an elderly user's health profile and returns a personalised, "
        "AI-generated 7-day meal plan with full nutritional breakdowns. "
        "The response is guaranteed to conform to the WeeklyMealPlan schema "
        "via OpenAI Structured Outputs."
    ),
    responses={
        200: {
            "description": "Successfully generated meal plan.",
            "model": GeneratePlanResponse,
        },
        422: {
            "description": "Validation error in request body.",
            "model": ErrorResponse,
        },
        500: {
            "description": "Internal server or AI service error.",
            "model": ErrorResponse,
        },
    },
)
async def generate_plan(profile: UserProfile) -> GeneratePlanResponse:
    """
    Generate a personalised 7-day dietary plan for an elderly user.

    The endpoint validates the incoming `UserProfile`, forwards it to the
    OpenAI service, and returns a structured `WeeklyMealPlan`.
    """
    try:
        logger.info(
            "Received plan request — age=%d, conditions=%s",
            profile.age,
            [d.value for d in profile.chronic_diseases],
        )

        meal_plan = await generate_meal_plan(profile)

        return GeneratePlanResponse(
            success=True,
            message="7-day meal plan generated successfully.",
            data=meal_plan,
        )

    except RuntimeError as exc:
        logger.error("Service error: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected error while generating meal plan")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {exc}",
        ) from exc


@router.get(
    "/health",
    summary="Health check",
    description="Returns the service health status.",
)
async def health_check() -> dict:
    """Simple liveness probe."""
    return {"status": "healthy", "service": "NutriElder AI Dietary Planner"}
