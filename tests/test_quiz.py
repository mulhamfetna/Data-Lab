from workshop import quiz


def test_every_epic_has_questions():
    assert len(quiz.epics()) >= 5
    for epic in quiz.epics():
        assert len(quiz.QUIZZES[epic]) >= 2


def test_all_correct_full_score():
    for epic in quiz.epics():
        answers = {i: q["best"] for i, q in enumerate(quiz.QUIZZES[epic])}
        r = quiz.grade_quiz(epic, answers)
        assert r["score"] == r["max"]


def test_wrong_and_missing_answers_not_scored():
    epic = quiz.epics()[0]
    q0 = quiz.QUIZZES[epic]
    answers = {0: (q0[0]["best"] + 1) % len(q0[0]["options"])}   # first wrong, rest missing
    r = quiz.grade_quiz(epic, answers)
    assert r["score"] == 0
    assert r["results"][0]["correct"] is False


def test_questions_well_formed():
    for epic in quiz.epics():
        for item in quiz.QUIZZES[epic]:
            assert 0 <= item["best"] < len(item["options"])
            assert item["q"] and item["why"]
