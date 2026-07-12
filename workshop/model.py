"""A small, honest classifier: predict whether a customer is 'high value'."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def build_features(df: pd.DataFrame):
    g = df.groupby("customer_name")
    feat = pd.DataFrame({
        "n_orders": g.size(),
        "total_qty": g["quantity"].sum(),
        "avg_amount": g["amount"].mean().round(2),
        "total_spend": g["amount"].sum().round(2),
    }).reset_index()
    # top city per customer (one-hot)
    top_city = g["city"].agg(lambda s: s.mode().iloc[0]).reset_index(name="top_city")
    feat = feat.merge(top_city, on="customer_name")
    city_dummies = pd.get_dummies(feat["top_city"], prefix="city")
    X = pd.concat([feat[["n_orders", "total_qty", "avg_amount"]], city_dummies], axis=1)
    y = (feat["total_spend"] >= feat["total_spend"].median()).astype(int)
    return X, y


def train(X: pd.DataFrame, y: pd.Series, seed: int = 0):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=seed)
    clf = RandomForestClassifier(n_estimators=120, random_state=seed)
    clf.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, clf.predict(X_te))
    importance = dict(sorted(zip(X.columns, clf.feature_importances_),
                             key=lambda kv: kv[1], reverse=True))
    return clf, {"accuracy": float(acc), "importance": importance, "columns": list(X.columns)}


def predict_one(model, features: dict, columns: list[str]) -> dict:
    row = pd.DataFrame([{c: features.get(c, 0) for c in columns}])
    label = int(model.predict(row)[0])
    proba = float(model.predict_proba(row)[0][1])
    return {"label": label, "proba": proba}
