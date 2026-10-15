from decimal import Decimal
from pytest import Mark
from susu_tracker.models import Member, Payout

#1. set up tracker class to manage the susu group
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
        # I use Decimal to avoid floating-point rounding errors. The validation also rejects contributions smaller than one pesewa.


#2. add members and record payments

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

        # Important design decision: I will be storing the current week's payment for each member. After a week closes successfully, I'll reset these balances for the new week.
        # This allows a member to pay GHS 30.00 first and GHS 20.00 later when the required contribution is GHS 50.00.


#3. Calculate outstanding balances

    def get_outstanding_balances(self) -> dict[str, Decimal]:
        return {
            member_id: self.weekly_contribution - paid
            for member_id, paid in self.weekly_payments.items()
            if paid < self.weekly_contribution
        }
    #This returns only the members who still owe money. 
    # For example, if Ama and Kofi have paid GHS 50.00 and Esi has paid GHS 30.00, the result will show that Esi owes GHS 20.00.


    #  Implement close_week

    def close_week(self) -> Payout:
        if self.rotation_complete:
            raise ValueError("The susu rotation is already complete.")

        if not self.members:
            raise ValueError("Cannot close a week without members.")

        outstanding = self.get_outstanding_balances()

        if outstanding:
            details = ", ".join(
                f"{self.members[member_id].name}: GHS {amount:.2f}"
                for member_id, amount in outstanding.items()
            )
            raise ValueError(f"Week {self.current_week} cannot close. Outstanding: {details}")

        recipient_id = list(self.members.keys())[
            len(self.payout_history)
        ]
        recipient = self.members[recipient_id]

        pot = self.weekly_contribution * len(self.members)

        payout = Payout(
            week=self.current_week,
            recipient_id=recipient.member_id,
            recipient_name=recipient.name,
            amount=pot,
        )

        self.payout_history.append(payout)
        self.current_week += 1
        self.weekly_payments = {
            member_id: Decimal("0.00")
            for member_id in self.members
        }

        if len(self.payout_history) == len(self.members):
            self.rotation_complete = True

        return payout

    # Understand the logic
    # 1. Reject closing if the rotation is already complete.
    # 2. Reject closing if the group has no members.
    # 3. Check outstanding balances. If anyone owes money, raise an error and leave the week unchanged.
    # 4. Select the next recipient in registration order.
    # 5. Calculate the pot as the weekly contribution multiplied by the number of members.
    # 6. Record the payout, advance the week, and reset weekly payments.
    # 7. Mark the rotation complete once every member has received the pot.
    
    # For this challenge, raising a ValueError when the week cannot close is a reasonable design. 
    # The command-line interface can catch that exception and display the outstanding amounts to the user.


    # Add the reporting method
    def get_report(self) -> dict:
        return {
            "current_week": self.current_week,
            "weekly_contribution": self.weekly_contribution,
            "rotation_complete": self.rotation_complete,
            "members": [
                {
                    "member_id": member.member_id,
                    "name": member.name,
                    "paid": self.weekly_payments[member_id],
                    "owes": self.weekly_contribution
                    - self.weekly_payments[member_id],
                }
                for member_id, member in self.members.items()
            ],
            "payout_history": list(self.payout_history),
        }
    #This gives us the information needed to display:
    # - The current week.
    # - Each member's payments and outstanding balance.
    # - Whether the rotation is complete.
    # - The full payout history.
    # A member who has paid in full will have an outstanding balance of Decimal("0.00").





    # Verify the tracker compiles
    # save and run; python -m py_compile susu_tracker/models.py susu_tracker/tracker.py

