from dataclasses import dataclass

from app.domain.leads import INTEREST_NAMES, Interest, InterestName


@dataclass(frozen=True, slots=True)
class InterestOption:
    value: Interest
    label: InterestName


class ListInterestOptions:
    def __call__(self) -> list[InterestOption]:
        return [
            InterestOption(value=interest, label=name) for interest, name in INTEREST_NAMES.items()
        ]
