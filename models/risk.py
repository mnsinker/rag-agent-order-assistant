from dataclasses import dataclass

@dataclass
class RiskResult:
    risk: bool
    reason: str