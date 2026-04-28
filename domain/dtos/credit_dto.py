from dataclasses import dataclass

@dataclass
class CreditScoreDTO:
    def __init__(self, score: int) -> None:
        self.score = score