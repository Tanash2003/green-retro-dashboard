# app.py
import streamlit as st
from utils.data_loader import load_csv

st.set_page_config(
    page_title="Green Retrofitting in UAE – Synthetic Analytics",
    layout="wide",
    page_icon="🌱",
)


def main():
    st.title("🌱 Green Retrofitting in UAE – Synthetic Analytics Dashboard")

    st.markdown("""
    ### Project Overview

    This dashboard presents insights from a **synthetic survey dataset of 600 responses**, 
    generated programmatically in Python for academic and exploratory purposes.

    ⚠️ **Important disclaimer:**
    - The dataset is **synthetic** and does **not** represent actual survey data or real individuals.
    - Any patterns or insights are **illustrative only** and **must not** be treated as real-world evidence.

    **Objective:**  
    Explore how building owners and occupants *might* behave in the context of green retrofitting in the UAE, 
    using analytics such as classification, clustering, and association rule mining (attempted).
    """)

    st.markdown("---")

    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        st.subheader("🔧 Analytics Included (Pre-computed Outside Streamlit)")

        st.markdown("""
        - **Classification models** (SVM, Random Forest, Gradient Boosting, Decision Tree, KNN, etc.)  
          • Trained offline on the synthetic dataset to predict adoption likelihood.  
          • Metrics are loaded from `classification_metrics.csv`.
        - **K-Means clustering**  
          • Behavioural segments based on preferences, motivations, and willingness to spend.  
          • Cluster profiles and demographic distributions are loaded from `cluster_profiles.csv` and `cluster_dist_by_*.csv`.
        - **Association Rule Mining (Apriori)**  
          • Attempted at **10% support** and **70% confidence**.  
          • **No rules were found** at these thresholds, suggesting strong co-occurrence patterns did not emerge in this synthetic data.
        """)

    with col_right:
        st.subheader("📊 Synthetic Dataset Snapshot")
        try:
            df = load_csv("green_retrofit_survey_synthetic.csv")
            total_rows = len(df)
            total_cols = df.shape[1]

            c1, c2 = st.columns(2)
            c1.metric("Synthetic responses", f"{total_rows}")
            c2.metric("Variables", f"{total_cols}")
            st.caption("Counts based on `green_retrofit_survey_synthetic.csv` in the `/data` folder.")
        except Exception:
            st.info("Base synthetic dataset not found yet. "
                    "Place `green_retrofit_survey_synthetic.csv` in `/data` to see summary stats here.")

    st.markdown("---")

    st.subheader("📁 How to Navigate")

    st.markdown("""
    - **Dataset Explorer:** Preview the synthetic survey data and apply basic filters.  
    - **Classification Analysis:** View model comparison metrics and ROC curves (images generated offline).  
    - **Clustering Segments:** Explore behavioural clusters, profiles, and demographic breakdowns.  
    - **Customer Lookup & Downloads:** Look up a synthetic respondent (placeholder prediction) and download CSV artifacts.
    """)


if __name__ == "__main__":
    main()
