from decimal import Decimal, InvalidOperation
from susu_tracker.tracker import SusuTracker


def read_amount(prompt: str) -> Decimal:
    """Read a monetary amount from the user."""
    value = input(prompt).strip()

    try:
        amount = Decimal(value)
    except InvalidOperation:
        raise ValueError("Enter a valid amount, such as 50.00.")

    if not amount.is_finite():
        raise ValueError("Amount must be a finite number.")

    return amount


def display_report(tracker: SusuTracker) -> None:
    """Display the current group status and payout history."""
    report = tracker.get_report()

    print("\n--- SUSU GROUP REPORT ---")
    print(f"Current week: {report['current_week']}")
    print(
        "Weekly contribution: "
        f"GHS {report['weekly_contribution']:.2f}"
    )

    if report["rotation_complete"]:
        print("Rotation status: Complete")
    else:
        print("Rotation status: In progress")

    print("\nMembers:")
    for member in report["members"]:
        print(
            f"- {member['name']} ({member['member_id']}): "
            f"Paid GHS {member['paid']:.2f}, "
            f"Owes GHS {member['owes']:.2f}"
        )

    print("\nPayout history:")
    if not report["payout_history"]:
        print("No payouts yet.")
    else:
        for payout in report["payout_history"]:
            print(
                f"- Week {payout.week}: {payout.recipient_name} "
                f"received GHS {payout.amount:.2f}"
            )


def run() -> None:
    """Run the Susu Group Tracker menu."""
    print("=== SUSU GROUP TRACKER ===")

    try:
        weekly_contribution = read_amount(
            "Enter the weekly contribution in GHS: "
        )
        tracker = SusuTracker(weekly_contribution)
    except ValueError as error:
        print(f"Error: {error}")
        return

    while True:
        print("\n1. Add member")
        print("2. Record contribution")
        print("3. Close current week")
        print("4. View report")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                member_id = input("Enter member ID: ").strip()
                name = input("Enter member name: ").strip()

                tracker.add_member(member_id, name)
                print(f"Member {name} added successfully.")

            elif choice == "2":
                member_id = input("Enter member ID: ").strip()
                amount = read_amount("Enter payment amount in GHS: ")

                tracker.record_contribution(member_id, amount)
                print("Contribution recorded successfully.")

            elif choice == "3":
                payout = tracker.close_week()
                print(
                    f"Week {payout.week} closed successfully. "
                    f"{payout.recipient_name} received "
                    f"GHS {payout.amount:.2f}."
                )

            elif choice == "4":
                display_report(tracker)

            elif choice == "5":
                print("Thank you for using the Susu Group Tracker.")
                break

            else:
                print("Invalid option. Choose a number from 1 to 5.")

        except (ValueError, InvalidOperation) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run()


#What this code does
# - read_amount() converts user input to Decimal.
# - display_report() presents member balances and payout history.
# - run() creates the tracker and manages the menu.
# - The try/except blocks catch invalid input and business-rule errors instead of crashing the program