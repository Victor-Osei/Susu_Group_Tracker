from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Member:
    member_id: str
    name: str


@dataclass
class Payout:
    week: int
    recipient_id: str
    recipient_name: str
    amount: Decimal

    # @dataclass generates useful methods for storing structured data.
    # Member represents a person participating in the susu group.
    # member_id provides a unique identifier, while name provides a readable name.
    # Payout records which week was paid, who received the pot, and the exact amount.
    # Decimal represents monetary values without the usual binary floating-point errors.