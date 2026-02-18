from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from backend.app.data.catalog import PRODUCT_CATALOG
from backend.app.schemas import ProductRecommendation, RecommendationRequest, RecommendationResponse


@dataclass
class ScoredItem:
    item: Dict
    score: float
    matched_features: List[str]


def _normalize(items: List[str]) -> List[str]:
    return [i.strip().lower() for i in items if i and i.strip()]


def _score_product(request: RecommendationRequest, product: Dict) -> ScoredItem:
    score = 0.0
    matched_features: List[str] = []

    # Budget proximity / fit
    if product["price"] <= request.budget:
        score += 35
        price_gap_ratio = (request.budget - product["price"]) / max(request.budget, 1)
        score += min(price_gap_ratio * 10, 10)
    else:
        over_ratio = (product["price"] - request.budget) / request.budget
        score -= min(over_ratio * 30, 25)

    preferred_brands = _normalize(request.preferred_brands)
    must_features = set(_normalize(request.must_have_features))
    nice_features = set(_normalize(request.nice_to_have_features))
    prod_features_map = {f.lower(): f for f in product.get("features", [])}
    prod_features = set(prod_features_map.keys())

    if preferred_brands and product["brand"].lower() in preferred_brands:
        score += 15

    must_matches = must_features.intersection(prod_features)
    missing_must = must_features.difference(prod_features)

    score += len(must_matches) * 12
    score -= len(missing_must) * 8
    matched_features.extend(prod_features_map[m] for m in sorted(must_matches))

    nice_matches = nice_features.intersection(prod_features)
    score += len(nice_matches) * 5
    matched_features.extend(prod_features_map[n] for n in sorted(nice_matches))

    use_case = (request.use_case or "").lower().strip()
    if use_case:
        if use_case in {"gaming", "design", "video editing"} and "dedicated gpu" in prod_features:
            score += 10
        if use_case in {"travel", "student"} and "lightweight" in prod_features:
            score += 8
        if use_case in {"photography", "content creation"} and (
            "excellent camera" in prod_features or "telephoto camera" in prod_features
        ):
            score += 10
        if use_case in {"long battery", "business"} and (
            "long battery" in prod_features or "5000mah battery" in prod_features
        ):
            score += 8

    return ScoredItem(item=product, score=round(score, 2), matched_features=matched_features)


def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    category = request.category.lower().strip()
    candidates = [p for p in PRODUCT_CATALOG if p["category"].lower() == category]

    if not candidates:
        return RecommendationResponse(
            summary=f"No products currently available for category '{request.category}'.",
            recommendations=[],
        )

    scored = [_score_product(request, p) for p in candidates]
    ranked = sorted(scored, key=lambda x: x.score, reverse=True)[: request.top_k]

    recommendations: List[ProductRecommendation] = []
    for row in ranked:
        product = row.item
        price_state = "within" if product["price"] <= request.budget else "slightly above"
        explanation = (
            f"{product['name']} is {price_state} your budget, scored {row.score}, "
            f"and matches key preferences: {', '.join(row.matched_features) if row.matched_features else 'general fit'}"
        )
        recommendations.append(
            ProductRecommendation(
                product_id=product["product_id"],
                name=product["name"],
                brand=product["brand"],
                category=product["category"],
                price=product["price"],
                score=row.score,
                matched_features=row.matched_features,
                explanation=explanation,
            )
        )

    summary = (
        f"Generated {len(recommendations)} recommendations for '{request.category}' "
        f"within/near budget ₹{request.budget:.0f} using preference-aware ranking."
    )

    return RecommendationResponse(summary=summary, recommendations=recommendations)
