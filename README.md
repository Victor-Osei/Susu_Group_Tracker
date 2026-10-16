# Susu Group Tracker

A Python command-line application for managing a rotating savings group (susu). Members contribute a fixed amount each week, and the entire pot is paid to one member in registration order.

## Features

- Create a group with a fixed weekly contribution in GHS.
- Register members with unique IDs.
- Record full and partial weekly contributions.
- Track outstanding balances.
- Prevent a week from closing when members still owe money.
- Pay the pot to the next eligible member in registration order.
- Display current group status and payout history.
- Validate invalid payments and member registrations.

## Requirements

- Python 3.10 or later
- pip

## Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Victor-Osei/Susu_Group_Tracker.git
cd Susu_Group_Tracker
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the application

From the project root:

```bash
python -m susu_tracker.cli
```

Follow the menu to add members, record contributions, close weeks, and view reports.

## Run the tests

Run the automated test suite with:

```bash
pytest -v
```

## Business Rules

- Every member contributes the same fixed amount each week.
- Partial payments are allowed.
- Payments must be positive, expressed in whole pesewas, and no greater than the member's outstanding balance.
- A week cannot close while any member owes money.
- Successful payouts follow member registration order.
- Each member receives the pot once per rotation.
- Members cannot be added after the first valid contribution starts the first week.

## Design Notes and Limitations

See [NOTES.md](NOTES.md) for assumptions, design decisions, known limitations, and possible future improvements.

The current version stores data in memory. Group records are not preserved after the application exits.