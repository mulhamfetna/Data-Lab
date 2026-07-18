"""Serving a model as an API: ship the model behind an endpoint anything can call."""
from workshop import model, store_data as sd


def build_service():
    df = sd.clean_orders(sd.messy_orders())
    X, y = model.build_features(df)
    clf, meta = model.train(X, y, seed=0)
    return clf, meta


def handle_request(payload: dict, clf, meta) -> dict:
    """Mimic an HTTP endpoint: validate the payload, predict, return a JSON-style response."""
    required = ["n_orders", "total_qty", "avg_amount"]
    missing = [k for k in required if k not in payload]
    if missing:
        return {"status": 400, "error": f"missing fields: {missing}"}
    out = model.predict_one(clf, payload, meta["columns"])
    return {"status": 200,
            "prediction": "high_value" if out["label"] == 1 else "regular",
            "confidence": round(out["proba"], 3)}
