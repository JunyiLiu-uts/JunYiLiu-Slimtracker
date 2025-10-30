from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class HealthRecord:
    date: str
    weight: float
    height: float
    bmi: float
    notes: Optional[str] = None
    id: Optional[int] = None
    
    @classmethod
    def create(cls, weight: float, height: float, notes: str = "") -> 'HealthRecord':
        bmi = cls.calculate_bmi(weight, height)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        return cls(current_date, weight, height, bmi, notes)
    
    @staticmethod
    def calculate_bmi(weight: float, height: float) -> float:
        return round(weight / (height ** 2), 2)