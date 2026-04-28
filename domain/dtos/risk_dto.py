from dataclasses import dataclass

@dataclass
class RiskResultDTO:
    risk: bool
    reason: str