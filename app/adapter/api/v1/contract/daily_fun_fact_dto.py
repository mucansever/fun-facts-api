from datetime import date
from pydantic import BaseModel

from app.domain.model import DailyFunFact


class DailyFunFactDto(BaseModel):
    date: date
    fact: str

    @staticmethod
    def from_model(model: DailyFunFact):
        return DailyFunFactDto(date=model.date, fact=model.fact)
