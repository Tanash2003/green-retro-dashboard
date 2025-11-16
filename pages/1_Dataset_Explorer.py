# pages/1_Dataset_Explorer.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_csv

def main():
    st.title("📊 Dataset Explorer (Synthetic Survey)")

    st.markdown("""
    Interact with the underlying **synthetic survey dataset**.  
    These records are artificially generated for learning and experimentation only.
    """)

    try:
        df = load_csv("green_retrofit_survey_synthetic.csv")
    except Exception:
        st.error(
            "Could not load `green_retrofit_survey_synthetic.csv` from `/data`. "
            "Make sure the file exists and the name matches."
        )
        return

    st.subheader("Dataset Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Synthetic respondents", len(df))
    col2.metric("Variables", df.shape[1])
    col3.metric("Total missing values", int(df.isna().sum().sum()))

    with st.expander("Show column info"):
        st.write(pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str),
            "num_unique": [df[c].nunique() for c in df.columns]
        }))

    st.markdown("---")
    st.subheader("Filter & Explore")

    # Simple filtering on low-cardinality / categorical-like columns
    categorical_cols = [
        c for c in df.columns
        if (df[c].dtype == "object") or (df[c].nunique() <= 12)
    ]

    st.caption("You can apply optional filters on selected categorical-like columns.")

    selected_cols = st.multiselect(
        "Columns to filter",
        options=categorical_cols,
    )

    filtered_df = df.copy()

    if selected_cols:
        st.markdown("#### Filters")
        for col in selected_cols:
            unique_vals = sorted(df[col].dropna().unique())
            selected_vals = st.multiselect(
                f"Values for `{col}`",
                options=unique_vals,
            )
            if selected_vals:
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

    st.markdown("### Data Preview")
    st.dataframe(filtered_df, use_container_width=True, height=450)

    st.markdown("### Summary Statistics")
    with st.expander("Numeric summary (describe)"):
        st.write(filtered_df.describe(include="number"))

    with st.expander("Categorical value counts (top 10 per column)"):
        for col in categorical_cols:
            st.markdown(f"**{col}**")
            st.write(filtered_df[col].value_counts().head(10))

    st.caption("All views are based on **synthetic data** only.")


if __name__ == "__main__":
    main()
