import os

import pandas as pd
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="GenAI Product Recommender", page_icon="🛍️", layout="wide")
st.title("🛍️ GenAI Product Recommendation System")
st.caption("Interactive recommendation assistant built with Streamlit + FastAPI")

with st.sidebar:
    st.header("User Constraints")
    category = st.selectbox("Category", ["laptop", "phone"])
    budget = st.number_input("Budget (INR)", min_value=1000, max_value=300000, value=60000, step=1000)
    preferred_brands = st.text_input("Preferred brands (comma-separated)", value="")
    must_have = st.text_input("Must-have features (comma-separated)", value="")
    nice_to_have = st.text_input("Nice-to-have features (comma-separated)", value="")
    use_case = st.selectbox(
        "Primary use case",
        ["general", "student", "travel", "gaming", "design", "video editing", "photography", "business"],
    )
    top_k = st.slider("Top recommendations", min_value=1, max_value=10, value=5)


def _split_csv(txt: str) -> list[str]:
    return [x.strip() for x in txt.split(",") if x.strip()]


if st.button("Get Recommendations", type="primary"):
    payload = {
        "budget": budget,
        "category": category,
        "preferred_brands": _split_csv(preferred_brands),
        "must_have_features": _split_csv(must_have),
        "nice_to_have_features": _split_csv(nice_to_have),
        "use_case": use_case,
        "top_k": top_k,
    }

    try:
        response = requests.post(f"{BACKEND_URL}/recommendations", json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        st.success(data["summary"])
        recs = data.get("recommendations", [])

        if not recs:
            st.info("No recommendations found for your current constraints.")
        else:
            table_df = pd.DataFrame(
                [
                    {
                        "Rank": idx + 1,
                        "Product": row["name"],
                        "Brand": row["brand"],
                        "Price": f"₹{row['price']:,.0f}",
                        "Score": row["score"],
                        "Matched Features": ", ".join(row["matched_features"]),
                    }
                    for idx, row in enumerate(recs)
                ]
            )
            st.subheader("Ranked Recommendations")
            st.dataframe(table_df, use_container_width=True, hide_index=True)

            st.subheader("Explainable Insights")
            for idx, row in enumerate(recs, 1):
                with st.expander(f"#{idx} {row['name']} — Score {row['score']}"):
                    st.write(row["explanation"])

    except requests.RequestException as exc:
        st.error(f"Could not connect to backend at {BACKEND_URL}. Error: {exc}")

with st.expander("API Endpoint"):
    st.code(f"POST {BACKEND_URL}/recommendations", language="bash")
