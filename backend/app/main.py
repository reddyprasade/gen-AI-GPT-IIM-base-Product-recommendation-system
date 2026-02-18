from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.recommendations import router as recommendation_router
from backend.app.schemas import HealthResponse

app = FastAPI(
    title="GenAI Product Recommendation API",
    description="FastAPI backend for constraint-aware product recommendations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


app.include_router(recommendation_router)
