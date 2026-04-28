from dataclasses import dataclass
@dataclass
class ShippingResultDTO:
    shipped: bool
    shipping_status: str