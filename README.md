# GenAI Product Recommendation System

This repository implements a **constraint-aware product recommendation system** using:
- **FastAPI** for backend recommendation APIs
- **Streamlit** for conversational-style user interaction and explainable ranked output

The app is aligned to the project goal in this repository: personalized, explainable recommendations based on budget, features, brand preference, and use-case constraints.

## Architecture

```text
[Streamlit UI] --> POST /recommendations --> [FastAPI API] --> [Ranking Service + Catalog] --> ranked recommendations + explanations
```

### Components
- `backend/app/main.py` – FastAPI app, health endpoint, CORS configuration.
- `backend/app/routes/recommendations.py` – Recommendation API route.
- `backend/app/services/recommender.py` – Scoring/ranking logic and explanations.
- `backend/app/data/catalog.py` – Sample in-memory product catalog.
- `frontend/streamlit_app.py` – Streamlit UI for collecting constraints and displaying results.

## Features

- Collects user constraints:
  - category
  - budget
  - preferred brands
  - must-have / nice-to-have features
  - use-case
- Produces ranked recommendations (`top_k`) with:
  - score
  - matched features
  - human-readable explanation
- Includes health endpoint for service monitoring.

## Setup

### 1) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2) Run backend (FastAPI)

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

### 3) Run frontend (Streamlit)

```bash
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

UI: `http://localhost:8501`

## API Contract

### `POST /recommendations`

Request:

```json
{
  "budget": 60000,
  "category": "laptop",
  "preferred_brands": ["Nova"],
  "must_have_features": ["512GB SSD"],
  "nice_to_have_features": ["long battery"],
  "use_case": "student",
  "top_k": 5
}
```

Response:

```json
{
  "summary": "Generated 3 recommendations for 'laptop' within/near budget ₹60000 using preference-aware ranking.",
  "recommendations": [
    {
      "product_id": "lap-002",
      "name": "NovaNote Air",
      "brand": "Nova",
      "category": "laptop",
      "price": 55999,
      "score": 72.33,
      "matched_features": ["512GB SSD", "long battery"],
      "explanation": "NovaNote Air is within your budget ..."
    }
  ]
}
```

## Environment Variables

Copy `.env.example` and customize as needed:
- `BACKEND_URL` for Streamlit-to-API communication.
- LLM-related placeholders are included for future enhancements.

## Developer Commands

```bash
make install
make run-backend
make run-frontend
make check
```

## Notes

- The current version uses an in-memory catalog and deterministic scoring for clarity and transparency.
- The design is ready to extend with LLM agents, vector search, or database-backed catalog retrieval.
