# pages/3_Clustering_Segments.py
import streamlit as st
from utils.data_loader import load_csv, get_asset_path, detect_cluster_column

def main():
    st.title("📌 Clustering Segments – Behavioural Profiles (Synthetic)")

    st.markdown("""
    K-Means clustering was applied offline to the **synthetic** dataset to identify behavioural segments.  
    Each cluster groups respondents with similar technology preferences, motivations, and spending patterns.
    """)

    # Load cluster profiles
    try:
        cluster_profiles = load_csv("cluster_profiles.csv")
    except Exception:
        st.error(
            "Could not load `cluster_profiles.csv` from the `/data` folder. "
            "Please ensure it exists and the filename is correct."
        )
        return

    st.subheader("📋 Cluster Profiles Table")
    st.caption("Each row represents one synthetic cluster with aggregated characteristics.")
    st.dataframe(cluster_profiles, use_container_width=True)

    # Detect cluster label column
    cluster_col = detect_cluster_column(cluster_profiles)

    st.markdown("---")
    st.subheader("📈 Visualisations of Clusters")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### PCA / 2D Cluster Plot")
        st.caption("Pre-computed PCA / cluster visualisation from the offline analysis.")
        try:
            pca_path = get_asset_path("pca_clusters.png")
            st.image(
                pca_path,
                use_container_width=True,
                caption="Synthetic clusters visualised in PCA space"
            )
        except Exception:
            st.info(
                "PCA cluster image not found in `/assets`. "
                "Save it as `pca_clusters.png` (or update the filename in this file)."
            )

    with col2:
        st.markdown("#### Additional Synthetic Charts")
        st.caption("Optional bar / pie charts summarising cluster adoption or preferences.")
        try:
            bar_path = get_asset_path("adoption_bar_chart.png")  # optional file
            st.image(
                bar_path,
                use_container_width=True,
                caption="Example synthetic chart (e.g., adoption rate by cluster)"
            )
        except Exception:
            st.info(
                "Optional chart (e.g., `adoption_bar_chart.png`) not found in `/assets`. "
                "You can add or rename images as needed."
            )

    st.markdown("---")
    st.subheader("👥 Explore Demographic Distribution by Cluster")

    st.markdown("""
    Choose:
    1. A demographic dimension (e.g., age group, income band), and  
    2. A specific cluster,  

    to view how synthetic respondents are distributed across that demographic within the selected cluster.
    """)

    # Expected file pattern: cluster_dist_by_<dimension>.csv
    dimension_options = [
        "age_group",
        "income_band",
        "emirate",
        "building_type",
    ]

    dim = st.selectbox(
        "Choose demographic dimension",
        options=dimension_options,
        index=0,
        help="Make sure a matching `cluster_dist_by_<dimension>.csv` exists in `/data`."
    )

    dist_filename = f"cluster_dist_by_{dim}.csv"

    try:
        dist_df = load_csv(dist_filename)
    except Exception:
        st.warning(
            f"Could not load `{dist_filename}` from `/data`. "
            "Export this file from your offline clustering script to enable this view."
        )
        return

    dist_cluster_col = detect_cluster_column(dist_df)
    available_clusters = sorted(dist_df[dist_cluster_col].unique())

    selected_cluster = st.selectbox(
        "Select cluster to inspect",
        options=available_clusters
    )

    cluster_slice = dist_df[dist_cluster_col == selected_cluster] if hasattr(dist_df, "__getitem__") else dist_df[dist_df[dist_cluster_col] == selected_cluster]

    st.markdown(f"#### Demographic breakdown for cluster `{selected_cluster}` (by `{dim}`)")
    st.dataframe(cluster_slice, use_container_width=True)

    st.caption("""
    Interpretation tips:
    - Identify which demographic categories dominate each cluster
      (e.g., high-income villa owners vs. younger apartment renters).  
    - Use this to shape synthetic segment narratives such as
      “Tech-savvy high-income homeowners” or “Budget-conscious tenants”.  
    - Reminder: this is **synthetic** data intended only for illustrating analysis workflows.
    """)


if __name__ == "__main__":
    main()
