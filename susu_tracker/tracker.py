from decimal import Decimal
from susu_tracker.models import Member, Payout

# set up tracker class to manage the susu group
class SusuTracker:
    def __init__(self, weekly_contribution: Decimal):
        if weekly_contribution <= Decimal("0.00"):
            raise ValueError("Weekly contribution must be positive.")

        if weekly_contribution.as_tuple().exponent < -2:
            raise ValueError("Contribution cannot have fractions of a pesewa.")

        self.weekly_contribution = weekly_contribution
        self.members = {}
        self.current_week = 1
        self.weekly_payments = {}
        self.payout_history = []
        self.rotation_complete = False
        self.week_started = False

        #What this establishes:
        # - weekly_contribution stores the fixed weekly amount.
        # - members stores registered members using their IDs as dictionary keys.
        # - current_week starts at week 1.
        # - weekly_payments tracks each member's payments for each week.
        # - payout_history records successful payouts.
        # - rotation_complete prevents additional payouts after everyone has received the pot.
        # - week_started helps us enforce the rule that members cannot be added after the first week starts.
        # We use Decimal to avoid floating-point rounding errors. The validation also rejects contributions smaller than one pesewa.


# add members and record payments

    def add_member(self, member_id: str, name: str) -> None:
        member_id = member_id.strip()
        name = name.strip()

        if not member_id or not name:
            raise ValueError("Member ID and name are required.")

        if member_id in self.members:
            raise ValueError("Member already exists.")

        if self.week_started:
            raise ValueError("Cannot add members after the first week starts.")

        self.members[member_id] = Member(member_id, name)
        self.weekly_payments[member_id] = Decimal("0.00")

    def record_contribution(self, member_id: str, amount: Decimal) -> None:
        if self.rotation_complete:
            raise ValueError("The susu rotation is complete.")

        if member_id not in self.members:
            raise ValueError("Unknown member.")

        if not amount.is_finite() or amount <= Decimal("0.00"):
            raise ValueError("Payment must be a positive amount.")

        if amount.as_tuple().exponent < -2:
            raise ValueError("Payment cannot have fractions of a pesewa.")

        current_payment = self.weekly_payments[member_id]
        outstanding = self.weekly_contribution - current_payment

        if amount > outstanding:
            raise ValueError("Payment exceeds the outstanding balance.")

        self.week_started = True
        self.weekly_payments[member_id] += amount

