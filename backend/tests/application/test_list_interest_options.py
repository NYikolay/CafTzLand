from application.leads import ListInterestOptions
from domain import Interest, InterestName


def test_lists_interest_options_with_russian_labels() -> None:
    options = ListInterestOptions()()

    assert [(option.value, option.label) for option in options] == [
        (Interest.SUBSCRIPTION, InterestName.SUBSCRIPTION),
        (Interest.ONE_TIME, InterestName.ONE_TIME),
        (Interest.QUESTION, InterestName.QUESTION),
    ]
