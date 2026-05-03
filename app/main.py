"""
NutriElder AI Dietary Planner — FastAPI Application Entry Point.

An AI-powered dietary planning assistant for the elderly that utilises
OpenAI Structured Outputs to generate safe, personalised 7-day nutritional
plans adapted to chronic conditions such as hypertension and diabetes.
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router

# ---------------------------------------------------------------------------
# Environment & Logging
# ---------------------------------------------------------------------------

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="🥗 NutriElder AI Dietary Planner API",
    description=(
        "An AI-powered dietary planning assistant for the elderly. "
        "Generates safe, personalised 7-day nutritional plans that adapt "
        "to chronic conditions (hypertension, diabetes, CKD, etc.) using "
        "OpenAI Structured Outputs.\n\n"
        "**Submitted for the OpenAI Codex × AIAT Hackathon**"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "NutriElder Team",
        "url": "https://github.com/NutriElder",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(api_router)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with basic service information."""
    return {
        "service": "NutriElder AI Dietary Planner API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


# ---------------------------------------------------------------------------
# Startup Event
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event() -> None:
    """Log service readiness on startup."""
    logger.info("🥗 NutriElder AI Dietary Planner API is starting up...")
    logger.info("📄 Interactive docs available at /docs")
