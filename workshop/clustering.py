"""Customer segmentation: find natural groups (tribes) with k-means."""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def customer_features(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("customer_name")
    return pd.DataFrame({
        "n_orders": g.size(),
        "total_spend": g["amount"].sum().round(2),
        "avg_amount": g["amount"].mean().round(2),
    }).reset_index()


def segment(features: pd.DataFrame, k: int = 3, seed: int = 0) -> pd.DataFrame:
    cols = ["n_orders", "total_spend", "avg_amount"]
    X = StandardScaler().fit_transform(features[cols])
    labels = KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(X)
    out = features.copy()
    out["segment"] = labels
    return out


def profiles(labeled: pd.DataFrame) -> pd.DataFrame:
    p = (labeled.groupby("segment")
         .agg(customers=("customer_name", "size"),
              avg_orders=("n_orders", "mean"),
              avg_spend=("total_spend", "mean"))
         .round(1).reset_index())
    return p
