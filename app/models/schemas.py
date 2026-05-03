"""
Pydantic data models for NutriElder AI Dietary Planner.

Defines strict schemas for user input (UserProfile) and
AI-generated output (WeeklyMealPlan) using Pydantic V2.
These models are also used with OpenAI Structured Outputs
to guarantee type-safe, validated JSON responses from the LLM.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ChronicDisease(str, Enum):
    """Common chronic conditions affecting dietary requirements in the elderly."""

    HYPERTENSION = "hypertension"
    DIABETES_TYPE_2 = "diabetes_type_2"
    CHRONIC_KIDNEY_DISEASE = "chronic_kidney_disease"
    HEART_DISEASE = "heart_disease"
    OSTEOPOROSIS = "osteoporosis"
    GOUT = "gout"
    DYSLIPIDEMIA = "dyslipidemia"
    OBESITY = "obesity"
    NONE = "none"


class PhysicalActivityLevel(str, Enum):
    """Physical activity level of the user."""

    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class UserProfile(BaseModel):
    """Input model describing the elderly user's health profile."""

    age: int = Field(
        ...,
        ge=60,
        le=120,
        description="Age of the elderly person (must be 60 or older).",
        json_schema_extra={"examples": [72]},
    )
    weight_kg: float = Field(
        ...,
        gt=0,
        le=300,
        description="Body weight in kilograms.",
        json_schema_extra={"examples": [68.5]},
    )
    height_cm: float = Field(
        ...,
        gt=0,
        le=250,
        description="Height in centimeters.",
        json_schema_extra={"examples": [165.0]},
    )
    chronic_diseases: list[ChronicDisease] = Field(
        default_factory=list,
        description="List of diagnosed chronic diseases.",
        json_schema_extra={"examples": [["hypertension", "diabetes_type_2"]]},
    )
    food_allergies: list[str] = Field(
        default_factory=list,
        description="Known food allergies or intolerances.",
        json_schema_extra={"examples": [["shellfish", "peanuts"]]},
    )
    activity_level: PhysicalActivityLevel = Field(
        default=PhysicalActivityLevel.SEDENTARY,
        description="Daily physical activity level.",
    )
    dietary_preferences: Optional[str] = Field(
        default=None,
        description="Optional dietary preferences (e.g., vegetarian, halal).",
        json_schema_extra={"examples": ["vegetarian"]},
    )

    model_config = {
        "json_schema_serialization_defaults_required": True,
    }


# ---------------------------------------------------------------------------
# Response Models (used as OpenAI Structured Output schema)
# ---------------------------------------------------------------------------

class NutritionalInfo(BaseModel):
    """Nutritional breakdown for a single meal."""

    calories_kcal: int = Field(..., description="Estimated calories in kcal.")
    protein_g: float = Field(..., description="Protein content in grams.")
    carbs_g: float = Field(..., description="Carbohydrate content in grams.")
    fat_g: float = Field(..., description="Fat content in grams.")
    sodium_mg: float = Field(..., description="Sodium content in milligrams.")
    fiber_g: float = Field(..., description="Fiber content in grams.")


class Meal(BaseModel):
    """A single meal with its details and nutritional information."""

    meal_name: str = Field(
        ...,
        description="Name of the dish (e.g., 'Steamed Salmon with Brown Rice').",
    )
    ingredients: list[str] = Field(
        ...,
        description="List of main ingredients used.",
    )
    preparation_notes: str = Field(
        ...,
        description="Brief cooking/preparation instructions.",
    )
    nutrition: NutritionalInfo = Field(
        ...,
        description="Nutritional breakdown of this meal.",
    )


class DailyMealPlan(BaseModel):
    """Complete meal plan for a single day."""

    day: str = Field(
        ...,
        description="Day label (e.g., 'Monday', 'Day 1').",
    )
    breakfast: Meal = Field(..., description="Breakfast meal.")
    morning_snack: Meal = Field(..., description="Mid-morning snack.")
    lunch: Meal = Field(..., description="Lunch meal.")
    afternoon_snack: Meal = Field(..., description="Afternoon snack.")
    dinner: Meal = Field(..., description="Dinner meal.")
    daily_calories_total: int = Field(
        ...,
        description="Total estimated calories for the day.",
    )
    daily_notes: str = Field(
        ...,
        description="Notes on hydration, medication timing, or other daily advice.",
    )


class WeeklyMealPlan(BaseModel):
    """Complete 7-day meal plan generated by the AI."""

    plan_title: str = Field(
        ...,
        description="Descriptive title for this meal plan.",
    )
    target_daily_calories: int = Field(
        ...,
        description="Recommended daily caloric target based on the user profile.",
    )
    medical_dietary_reasoning: str = Field(
        ...,
        description=(
            "Explanation of how the plan adapts to the user's chronic diseases "
            "and allergies. Must address each condition specifically."
        ),
    )
    general_guidelines: list[str] = Field(
        ...,
        description="General nutritional guidelines tailored to the user.",
    )
    days: list[DailyMealPlan] = Field(
        ...,
        min_length=7,
        max_length=7,
        description="Exactly 7 daily meal plans (Monday through Sunday).",
    )
    disclaimer: str = Field(
        ...,
        description=(
            "Medical disclaimer advising the user to consult a healthcare "
            "professional before following this plan."
        ),
    )


# ---------------------------------------------------------------------------
# API Response Wrapper
# ---------------------------------------------------------------------------

class GeneratePlanResponse(BaseModel):
    """Top-level API response returned by the /generate-plan endpoint."""

    success: bool = Field(..., description="Whether the request succeeded.")
    message: str = Field(..., description="Human-readable status message.")
    data: Optional[WeeklyMealPlan] = Field(
        default=None,
        description="The generated 7-day meal plan (null on error).",
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    success: bool = Field(default=False)
    message: str = Field(..., description="Error description.")
    detail: Optional[str] = Field(
        default=None,
        description="Detailed technical error information.",
    )
