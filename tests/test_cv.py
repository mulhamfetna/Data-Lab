from workshop import cv


def test_model_learns_digits():
    m = cv.train(seed=0)
    assert m["accuracy"] > 0.9        # digits is an easy, real CV benchmark


def test_predict_returns_a_digit():
    m = cv.train(seed=0)
    p = cv.predict(m["clf"], m["Xte"][0])
    assert p in range(10)
