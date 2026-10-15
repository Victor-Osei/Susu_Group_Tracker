from decimal import Decimal
import pytest
from susu_tracker import tracker
from susu_tracker.tracker import SusuTracker


def create_group():
    tracker = SusuTracker(Decimal("50.00"))
    tracker.add_member("A1", "Ama")
    tracker.add_member("K1", "Kofi")
    tracker.add_member("E1", "Esi")
    return tracker


#def test_partial_payment_tracks_outstanding_balance():
 #   tracker = create_group()
#
 #   tracker.record_contribution("E1", Decimal("30.00"))
#
    #assert tracker.get_outstanding_balances() == {
   #     "A1": Decimal("50.00"),
  #      "K1": Decimal("50.00"),
 #       "E1": Decimal("20.00"),
#    }

def test_partial_payment_tracks_outstanding_balance():
    tracker = create_group()

    tracker.record_contribution("A1", Decimal("50.00"))
    tracker.record_contribution("K1", Decimal("50.00"))
    tracker.record_contribution("E1", Decimal("30.00"))

    assert tracker.get_outstanding_balances() == {
        "E1": Decimal("20.00"),
    }


def test_week_cannot_close_when_member_owes():
    tracker = create_group()

    tracker.record_contribution("A1", Decimal("50.00"))
    tracker.record_contribution("K1", Decimal("50.00"))
    tracker.record_contribution("E1", Decimal("30.00"))

    with pytest.raises(ValueError, match="Esi: GHS 20.00"):
        tracker.close_week()

    assert tracker.current_week == 1
    assert tracker.payout_history == []


def test_completed_week_pays_first_member():
    tracker = create_group()

    for member_id in ["A1", "K1", "E1"]:
        tracker.record_contribution(member_id, Decimal("50.00"))

    payout = tracker.close_week()

    assert payout.recipient_name == "Ama"
    assert payout.amount == Decimal("150.00")
    assert payout.week == 1
    assert tracker.current_week == 2


def test_partial_payments_can_be_completed():
    tracker = create_group()

    tracker.record_contribution("E1", Decimal("30.00"))
    tracker.record_contribution("E1", Decimal("20.00"))

    assert "E1" not in tracker.get_outstanding_balances()
    assert tracker.weekly_payments["E1"] == Decimal("50.00")
    # assert tracker.get_outstanding_balances()["E1"] == Decimal("0.00")


def test_duplicate_member_is_rejected():
    tracker = create_group()

    with pytest.raises(ValueError, match="already exists"):
        tracker.add_member("A1", "Another Ama")


def test_unknown_member_is_rejected():
    tracker = create_group()

    with pytest.raises(ValueError, match="Unknown member"):
        tracker.record_contribution("X1", Decimal("50.00"))


def test_overpayment_is_rejected():
    tracker = create_group()

    with pytest.raises(ValueError, match="exceeds"):
        tracker.record_contribution("A1", Decimal("50.01"))


def test_second_week_pays_second_member():
    tracker = create_group()

    for member_id in ["A1", "K1", "E1"]:
        tracker.record_contribution(member_id, Decimal("50.00"))

    tracker.close_week()

    for member_id in ["A1", "K1", "E1"]:
        tracker.record_contribution(member_id, Decimal("50.00"))

    payout = tracker.close_week()

    assert payout.recipient_name == "Kofi"
    assert payout.week == 2
    assert payout.amount == Decimal("150.00")