"""Interactive labeling: humans tag examples, a model learns from the labels."""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# The review pool with hidden TRUE sentiment (1 = positive, 0 = negative).
POOL: list[tuple[str, int]] = [
    ("loved it will buy again", 1), ("fast delivery great value", 1),
    ("friendly and helpful support", 1), ("excellent quality product", 1),
    ("amazing highly recommend", 1), ("quick and reliable service", 1),
    ("best store in aleppo", 1), ("great price worth every lira", 1),
    ("smooth easy order", 1), ("very satisfied thank you", 1),
    ("delivery was slow", 0), ("poor unhelpful support", 0),
    ("product broke quickly", 0), ("too expensive not worth it", 0),
    ("late and damaged", 0), ("bad experience overall", 0),
    ("never buying again", 0), ("wrong item was sent", 0),
    ("rude staff", 0), ("took forever to arrive", 0),
]


def train_and_eval(labeled: list[tuple[str, int]]) -> dict | None:
    """Train on the human-labeled examples; evaluate on the whole pool's true labels.

    Returns None until at least one example of each class is labeled.
    """
    labels = [lbl for _, lbl in labeled]
    if len(set(labels)) < 2:
        return None
    vec = CountVectorizer()
    X = vec.fit_transform([t for t, _ in labeled])
    clf = LogisticRegression(max_iter=1000).fit(X, labels)
    Xp = vec.transform([t for t, _ in POOL])
    pred = clf.predict(Xp)
    acc = accuracy_score([lbl for _, lbl in POOL], pred)
    return {"accuracy": float(acc), "n_labeled": len(labeled)}
