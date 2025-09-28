from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DailyFunFact:
    date: date
    fact: str

    @staticmethod
    def from_ordinal(ordinal: int, fact: str) -> 'DailyFunFact':
        return DailyFunFact(date=date.fromordinal(ordinal), fact=fact)