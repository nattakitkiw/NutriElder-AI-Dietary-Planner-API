# 🥗 NutriElder-AI-Dietary-Planner-API

> **AI-Powered Dietary Planning for Elderly Care in the Post-AGI Era**
>
> Submitted for the **OpenAI Codex × AIAT Hackathon** — *Wellness AI in the Post-AGI Era*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-Structured%20Outputs-412991?logo=openai&logoColor=white)](https://platform.openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Overview

**NutriElder** is an AI-powered REST API that generates **safe, personalised 7-day meal plans** for elderly individuals (60+). It leverages OpenAI's **Structured Outputs** feature to guarantee that every AI response strictly conforms to a medically-aware nutritional schema — no hallucinated formats, no missing fields, no unsafe recommendations.

### ✨ Key Features

- 🧬 **Chronic Disease Adaptation** — Automatically adjusts meals for hypertension, diabetes, CKD, heart disease, osteoporosis, gout, and more
- 🚫 **Allergy-Safe Guarantees** — Food allergies are embedded in the AI prompt to prevent any unsafe ingredient from appearing
- 📊 **Full Nutritional Breakdown** — Every meal includes calories, protein, carbs, fat, sodium, and fiber data
- 🔒 **Schema-Guaranteed Responses** — OpenAI Structured Outputs ensure the JSON response always matches the Pydantic model
- 📅 **Complete 7-Day Plans** — Breakfast, morning snack, lunch, afternoon snack, and dinner for each day
- ⚡ **Production-Ready API** — Built with FastAPI, async-first, with CORS support and interactive docs

---

## 🌍 Impact on Aging Society

The world is aging rapidly. By 2050, over **2.1 billion people** will be aged 60 or older (WHO). Malnutrition among the elderly is a silent crisis — contributing to falls, cognitive decline, weakened immunity, and hospital readmissions.

### Why Structured AI Outputs Matter for Elderly Nutrition

| Challenge | How NutriElder Solves It |
|---|---|
| **Unsafe AI recommendations** | Structured Outputs *enforce* a validated schema — the AI cannot return incomplete or malformed dietary advice |
| **Ignoring chronic conditions** | The system prompt and user profile explicitly encode diseases, making condition-aware meal planning mandatory |
| **Food allergy risks** | Allergies are passed directly to the LLM with strict avoidance instructions |
| **Inconsistent nutritional data** | Every meal includes a `NutritionalInfo` object with enforced numeric fields |
| **Caregiver trust** | A medical disclaimer is *required* by the schema — it cannot be omitted |

> **The key insight:** In healthcare AI, *format reliability* is just as critical as *content accuracy*. By using Structured Outputs, we eliminate an entire class of failure modes where the AI might return unusable, unparseable, or dangerously incomplete dietary advice.

---

## 🏗️ Architecture

```
NutriElder-AI-Dietary-Planner-API/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py         # API route definitions
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic data models
│   └── services/
│       ├── __init__.py
│       └── openai_service.py    # OpenAI Structured Outputs integration
├── .env.example                 # Environment variable template
├── .gitignore                   # Python gitignore
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Local Setup

### Prerequisites

- Python 3.11 or newer
- An [OpenAI API Key](https://platform.openai.com/api-keys) with access to `gpt-4o`

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/NutriElder-AI-Dietary-Planner-API.git
cd NutriElder-AI-Dietary-Planner-API
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key
```

### Step 5 — Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6 — Explore the API

- **Interactive Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 📡 API Documentation

### `POST /api/v1/generate-plan`

Generate a personalised 7-day meal plan for an elderly user.

#### Request Body

```json
{
  "age": 72,
  "weight_kg": 68.5,
  "height_cm": 165.0,
  "chronic_diseases": ["hypertension", "diabetes_type_2"],
  "food_allergies": ["shellfish", "peanuts"],
  "activity_level": "sedentary",
  "dietary_preferences": "No specific preferences"
}
```

#### cURL Example

```bash
curl -X POST http://localhost:8000/api/v1/generate-plan \
  -H "Content-Type: application/json" \
  -d '{
    "age": 72,
    "weight_kg": 68.5,
    "height_cm": 165.0,
    "chronic_diseases": ["hypertension", "diabetes_type_2"],
    "food_allergies": ["shellfish", "peanuts"],
    "activity_level": "sedentary",
    "dietary_preferences": null
  }'
```

#### Successful Response (200 OK)

```json
{
  "success": true,
  "message": "7-day meal plan generated successfully.",
  "data": {
    "plan_title": "7-Day Heart & Diabetes-Friendly Meal Plan for Elderly",
    "target_daily_calories": 1600,
    "medical_dietary_reasoning": "This plan limits sodium to <1500mg/day for hypertension management and uses low-GI carbohydrates for blood sugar control...",
    "general_guidelines": [
      "Drink at least 8 glasses of water daily",
      "Eat meals at consistent times to stabilize blood sugar",
      "..."
    ],
    "days": [
      {
        "day": "Monday",
        "breakfast": {
          "meal_name": "Oatmeal with Blueberries and Flaxseed",
          "ingredients": ["rolled oats", "blueberries", "ground flaxseed", "almond milk"],
          "preparation_notes": "Cook oats with almond milk, top with berries and flaxseed.",
          "nutrition": {
            "calories_kcal": 280,
            "protein_g": 8.5,
            "carbs_g": 42.0,
            "fat_g": 7.5,
            "sodium_mg": 45.0,
            "fiber_g": 6.2
          }
        },
        "morning_snack": { "..." : "..." },
        "lunch": { "..." : "..." },
        "afternoon_snack": { "..." : "..." },
        "dinner": { "..." : "..." },
        "daily_calories_total": 1580,
        "daily_notes": "Remember to take blood pressure medication with breakfast."
      }
    ],
    "disclaimer": "This meal plan is AI-generated and intended for informational purposes only. Please consult your physician or a registered dietitian before making dietary changes."
  }
}
```

#### Error Response (500)

```json
{
  "detail": "OpenAI API error: ..."
}
```

### `GET /api/v1/health`

Health check endpoint.

```bash
curl http://localhost:8000/api/v1/health
```

```json
{
  "status": "healthy",
  "service": "NutriElder AI Dietary Planner"
}
```

---

## 🧩 Supported Chronic Diseases

| Disease | Dietary Adaptations |
|---|---|
| **Hypertension** | Low sodium (< 1,500 mg/day), potassium-rich foods |
| **Diabetes Type 2** | Low glycaemic index, controlled carbohydrates |
| **Chronic Kidney Disease** | Limited protein, potassium, and phosphorus |
| **Heart Disease** | Low saturated fat, high omega-3 |
| **Osteoporosis** | High calcium & vitamin D |
| **Gout** | Avoid purine-rich foods |
| **Dyslipidemia** | Low trans fat, high soluble fiber |
| **Obesity** | Calorie-controlled portions |

---

## 🛡️ Tech Stack

| Component | Technology |
|---|---|
| **Backend Framework** | FastAPI |
| **Data Validation** | Pydantic V2 |
| **AI Engine** | OpenAI GPT-4o with Structured Outputs |
| **Async Runtime** | Uvicorn (ASGI) |
| **Config Management** | python-dotenv |

---

## ⚠️ Disclaimer

This project generates AI-powered dietary recommendations for **informational and educational purposes only**. It is **not a substitute for professional medical advice**, diagnosis, or treatment. Always consult a qualified healthcare provider before making changes to a diet, especially for individuals with chronic health conditions.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ for the elderly community<br/>
  <strong>OpenAI Codex × AIAT Hackathon 2025</strong>
</p>
