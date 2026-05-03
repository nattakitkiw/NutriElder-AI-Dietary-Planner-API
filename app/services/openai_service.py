"""
OpenAI service for generating structured dietary plans.

Uses OpenAI's Structured Outputs (response_format with a Pydantic model)
to guarantee that every LLM response strictly conforms to the
WeeklyMealPlan schema — no post-hoc parsing or retry logic needed.
"""

from __future__ import annotations

import logging
import os

from openai import AsyncOpenAI, OpenAIError

from app.models.schemas import UserProfile, WeeklyMealPlan

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Client initialisation
# ---------------------------------------------------------------------------

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    """Return a lazily-initialised async OpenAI client."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. "
                "Please add it to your .env file."
            )
        _client = AsyncOpenAI(api_key=api_key)
    return _client


def _get_model() -> str:
    """Return the configured model name, defaulting to gpt-4o."""
    return os.getenv("OPENAI_MODEL", "gpt-4o")


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are NutriElder AI — a certified clinical dietitian AI specialised in \
elderly nutrition (age 60+). Your role is to generate safe, evidence-based, \
personalised 7-day meal plans.

STRICT RULES:
1. Every recommendation MUST respect the patient's chronic diseases. For example:
   - Hypertension  → limit sodium to < 1,500 mg/day, emphasise potassium-rich foods.
   - Diabetes Type 2 → low glycaemic index meals, controlled carbohydrate portions.
   - Chronic Kidney Disease → limit protein, potassium, and phosphorus.
   - Heart Disease → low saturated fat, high omega-3 fatty acids.
   - Osteoporosis → high calcium & vitamin D foods.
   - Gout → avoid purine-rich foods (organ meats, shellfish).
   - Dyslipidemia → limit trans fats, increase soluble fibre.
2. NEVER include any food the patient is allergic to. Double-check every ingredient.
3. Meals must be soft-textured or easy to chew when appropriate for elderly patients.
4. Ensure adequate hydration advice in daily notes.
5. Include a clear medical disclaimer.
6. Provide realistic portion sizes for elderly individuals.
7. Calculate nutritional values as accurately as possible.
8. Respect dietary preferences if provided.
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def generate_meal_plan(profile: UserProfile) -> WeeklyMealPlan:
    """
    Generate a personalised 7-day meal plan using OpenAI Structured Outputs.

    Parameters
    ----------
    profile : UserProfile
        The elderly user's health and dietary profile.

    Returns
    -------
    WeeklyMealPlan
        A validated, schema-conformant weekly meal plan.

    Raises
    ------
    RuntimeError
        If the OpenAI API call fails or returns an unexpected response.
    """
    client = _get_client()
    model = _get_model()

    user_message = _build_user_message(profile)

    logger.info(
        "Requesting meal plan from OpenAI (%s) for user age=%d",
        model,
        profile.age,
    )

    try:
        completion = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            response_format=WeeklyMealPlan,
            temperature=0.6,
        )

        meal_plan = completion.choices[0].message.parsed

        if meal_plan is None:
            refusal = completion.choices[0].message.refusal
            raise RuntimeError(
                f"The model refused to generate a plan: {refusal}"
            )

        logger.info("Successfully generated meal plan: %s", meal_plan.plan_title)
        return meal_plan

    except OpenAIError as exc:
        logger.error("OpenAI API error: %s", exc)
        raise RuntimeError(f"OpenAI API error: {exc}") from exc


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_user_message(profile: UserProfile) -> str:
    """Compose a detailed user message from the health profile."""
    diseases = (
        ", ".join(d.value for d in profile.chronic_diseases)
        if profile.chronic_diseases
        else "None reported"
    )
    allergies = (
        ", ".join(profile.food_allergies)
        if profile.food_allergies
        else "None reported"
    )
    preferences = profile.dietary_preferences or "No specific preferences"

    # Basic BMI for context
    height_m = profile.height_cm / 100
    bmi = round(profile.weight_kg / (height_m ** 2), 1)

    return (
        f"Please generate a personalised 7-day meal plan for the following "
        f"elderly patient:\n\n"
        f"• Age: {profile.age} years old\n"
        f"• Weight: {profile.weight_kg} kg\n"
        f"• Height: {profile.height_cm} cm\n"
        f"• BMI: {bmi}\n"
        f"• Chronic diseases: {diseases}\n"
        f"• Food allergies / intolerances: {allergies}\n"
        f"• Physical activity level: {profile.activity_level.value}\n"
        f"• Dietary preferences: {preferences}\n\n"
        f"Ensure the plan is safe, nutritionally balanced, and adapted to ALL "
        f"of the conditions listed above. Provide specific reasoning for each "
        f"dietary adaptation in the medical_dietary_reasoning field."
    )
