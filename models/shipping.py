from dataclasses import dataclass
@dataclass
class ShippingResult():
    shipped: bool
    shipping_status: str