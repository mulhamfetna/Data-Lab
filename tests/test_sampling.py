from workshop import sampling as sm


def test_bias_inflates_the_estimate():
    pop = sm.population()
    unbiased = sm.estimates(pop, sm.biased_sample(pop, 0.0))
    biased = sm.estimates(pop, sm.biased_sample(pop, 3.0))
    assert abs(unbiased["gap"]) < 5            # fair sample ≈ truth
    assert biased["gap"] > 5                    # biased sample overshoots
