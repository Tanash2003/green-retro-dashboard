# utils/data_loader.py
import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"


@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV from the /data folder with caching.
    """
    path = DATA_DIR / filename
    return pd.read_csv(path)


def get_asset_path(filename: str) -> str:
    """
    Get the full path to an image in the /assets folder.
    """
    return str(ASSETS_DIR / filename)


def detect_cluster_column(df: pd.DataFrame) -> str:
    """
    Try to detect a cluster/segment label column.
    """
    candidates = [c for c in df.columns if "cluster" in c.lower() or "segment" in c.lower()]
    if candidates:
        return candidates[0]
    return df.columns[0]


def detect_id_column(df: pd.DataFrame) -> str:
    """
    Try to detect an ID column.
    """
    candidates = [c for c in df.columns if "id" in c.lower()]
    if candidates:
        return candidates[0]
    return df.columns[0]
