# pages/2_Classification_Analysis.py
import streamlit as st
from utils.data_loader import load_csv, get_asset_path

def main():
    st.title("🤖 Classification Analysis – Adoption Likelihood (Synthetic)")

    st.markdown("""
    This page summarises *offline* model results trained on the **synthetic** survey dataset.  
    Models such as SVM, Random Forest, Gradient Boosting, Decision Tree, and KNN were
    **trained outside Streamlit**.  
    The app only loads their **metrics** and **ROC curve image** – it does not retrain any models.
    """)

    # Load pre-computed metrics
    try:
        metrics_df = load_csv("classification_metrics.csv")
    except Exception:
        st.error(
            "Could not load `classification_metrics.csv` from the `/data` folder. "
            "Please ensure it exists and the filename is correct."
        )
        return

    st.subheader("📋 Model Performance Table")

    # Identify metric vs non-metric columns
    non_metric_cols = [c for c in metrics_df.columns if c.lower() in ["model", "algorithm", "name"]]
    metric_cols = [c for c in metrics_df.columns if c not in non_metric_cols]

    col1, col2 = st.columns(2)
    with col1:
        sort_col = st.selectbox(
            "Sort models by metric",
            options=metric_cols if metric_cols else metrics_df.columns,
            index=0
        )
    with col2:
        order = st.radio(
            "Sort order",
            ["Descending (best first)", "Ascending"],
            index=0,
            horizontal=True
        )
    ascending = order == "Ascending"

    metrics_sorted = metrics_df.sort_values(by=sort_col, ascending=ascending)
    st.dataframe(metrics_sorted, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 ROC Curve (Offline Image)")

    st.caption("""
    The ROC curve below was generated as part of the offline modelling workflow
    and saved as a PNG file. Streamlit simply displays the pre-computed image
    from the `/assets` folder.
    """)

    try:
        roc_path = get_asset_path("roc_curve.png")  # change file name here if needed
        st.image(
            roc_path,
            use_container_width=True,
            caption="ROC curves for classification models on the synthetic dataset"
        )
    except Exception:
        st.info(
            "ROC curve image not found in `/assets`. "
            "Save it as `roc_curve.png` (or update the filename in this file)."
        )

    st.markdown("---")
    st.subheader("🧩 Interpretation (High-level, Synthetic-only)")

    st.markdown("""
    - **Compare models on multiple metrics:**  
      Focus on metrics like accuracy, F1-score, and ROC-AUC to see which model performs
      best on the synthetic adoption prediction task.
    - **Interpretability vs. performance trade-off:**  
      - Tree-based models (e.g., Decision Tree) tend to be easier to explain but may have
        slightly lower performance.  
      - Ensemble models (Random Forest, Gradient Boosting) often perform better but are
        more complex.
    - **Synthetic context reminder:**  
      All metrics shown here reflect performance on **synthetic data only** and are intended
      purely for demonstration. They must not be used for real-world decisions.
    """)


if __name__ == "__main__":
    main()
