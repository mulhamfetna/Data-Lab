"""Image classification on the classic handwritten-digits dataset (a real, small CV task)."""
import numpy as np
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train(seed: int = 0) -> dict:
    d = load_digits()
    idx = np.arange(len(d.data))
    Xtr, Xte, ytr, yte, _, ite = train_test_split(
        d.data, d.target, idx, test_size=0.3, random_state=seed)
    clf = RandomForestClassifier(n_estimators=120, random_state=seed).fit(Xtr, ytr)
    acc = accuracy_score(yte, clf.predict(Xte))
    return {"clf": clf, "Xte": Xte, "yte": yte, "images": d.images[ite], "accuracy": float(acc)}


def predict(clf, x) -> int:
    return int(clf.predict([x])[0])
