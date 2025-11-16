# pages/4_Customer_Lookup_and_Downloads.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_csv, detect_id_column

def main():
    st.title("🔍 Customer Lookup (Synthetic) & Downloads")

    st.markdown("""
    Use this page to:
    - Look up an individual **synthetic respondent**, and  
    - Download the main CSV outputs used in this dashboard.

    No real customer data is involved – all records are **synthetic**.
    """)

    # Try loading base synthetic survey
    survey_df = None
    try:
        survey_df = load_csv("green_retrofit_survey_synthetic.csv")
    except Exception:
        st.warning("Could not load `green_retrofit_survey_synthetic.csv`. "
                   "Lookup will be disabled but downloads may still work.")

    # --- Customer lookup (placeholder) ---
    st.subheader("👤 Synthetic Respondent Lookup")

    if survey_df is not None:
        id_col = detect_id_column(survey_df)
        st.caption(f"Using `{id_col}` as the respondent identifier.")

        all_ids = survey_df[id_col].tolist()
        selected_id = st.selectbox("Select synthetic respondent ID", options=all_ids)

        respondent_row = survey_df[survey_df[id_col] == selected_id]
        st.markdown("#### Respondent details (synthetic)")
        st.dataframe(respondent_row, use_container_width=True)

        st.markdown("#### Adoption probability (placeholder)")

        st.info("""
        This is currently a **placeholder** for a predicted adoption probability.
        Once you have a CSV with predictions (e.g., `synthetic_predictions.csv` containing 
        columns like respondent ID and adoption_probability), you can:
        1. Load that CSV here, and  
        2. Join it on the respondent ID to display the actual predicted probability.
        """)

        # Simple placeholder slider so UI feels complete
        placeholder_prob = st.slider(
            "Illustrative adoption probability (for demonstration only)",
            min_value=0.0,
            max_value=1.0,
            value=0.65,
            step=0.01
        )
        st.write(f"**Displayed synthetic probability:** {placeholder_prob:.2%}")
    else:
        st.info("Synthetic survey not loaded – respondent lookup is skipped.")

    st.markdown("---")
    st.subheader("⬇️ Download CSV Artifacts")

    st.markdown("You can download key CSV files used in this project (all derived from synthetic data).")

    download_files = {
        "Base synthetic survey": "green_retrofit_survey_synthetic.csv",
        "Classification metrics": "classification_metrics.csv",
        "Cluster profiles": "cluster_profiles.csv",
        # Add more as needed:
        # "Cluster dist by age group": "cluster_dist_by_age_group.csv",
        # "Cluster dist by income band": "cluster_dist_by_income_band.csv",
    }

    for label, filename in download_files.items():
        try:
            df = load_csv(filename)
        except Exception:
            st.warning(f"Could not load `{filename}` – skipping download button.")
            continue

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download {label} (`{filename}`)",
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
        )

    st.caption("All downloadable files are based on **synthetic** data created solely for demonstration.")


if __name__ == "__main__":
    main()
