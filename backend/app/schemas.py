from typing import List, Optional

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0, description="Maximum budget in INR")
    category: str = Field(..., description="Product category (e.g., laptop, phone)")
    preferred_brands: List[str] = Field(default_factory=list)
    must_have_features: List[str] = Field(default_factory=list)
    nice_to_have_features: List[str] = Field(default_factory=list)
    use_case: Optional[str] = Field(default="general")
    top_k: int = Field(default=5, ge=1, le=10)


class ProductRecommendation(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    price: float
    score: float
    matched_features: List[str]
    explanation: str


class RecommendationResponse(BaseModel):
    summary: str
    recommendations: List[ProductRecommendation]


class HealthResponse(BaseModel):
    status: str
