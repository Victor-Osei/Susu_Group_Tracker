# Design Notes

## Assumptions and Decisions

1. The application manages one susu group per program session.
2. Each member has a unique ID and a name.
3. Members can be added before the first valid contribution is recorded. Once a week starts, membership is fixed.
4. Each member must contribute the same fixed amount every week.
5. Partial payments are allowed and accumulate toward the weekly contribution.
6. A payment must be positive, must not exceed the outstanding balance, and must be expressed in whole pesewas.
7. A week cannot close if any member has an outstanding balance. No payout occurs in that case.
8. The payout recipient is determined by registration order.
9. The weekly pot equals the fixed contribution multiplied by the number of registered members.
10. After a successful payout, the next week begins and weekly payment balances reset.
11. The rotation ends after every member has received the pot once.
12. Monetary values use Python's Decimal type to avoid binary floating-point rounding errors.
13. Group data is stored in memory and is lost when the program exits.

## Known Limitations

- Data is not persisted between program sessions.
- The application supports one group at a time.
- There is no authentication or role-based access control.
- Contributions and payouts are not stored in a permanent transaction ledger.

## Future Improvements

- Persist members, contributions, and payouts using SQLite.
- Add transaction IDs and timestamps.
- Improve input handling and reporting.
- Add tests for persistence and recovery.
- Support multiple groups if required.
- Add an audit trail for changes and payouts.