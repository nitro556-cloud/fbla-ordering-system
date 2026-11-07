# Test results — November 6, 2026

Command: `.venv/bin/python -m unittest -v test_app`

Final result: **12 test groups passed, 0 failures, 0 errors**. The final run completed in 0.120 seconds using Flask 3.1.2 on Python 3.13. Tests use Flask's test client and temporary JSON files, leaving demo inventory untouched.

| Requested behavior | Result |
| --- | --- |
| Empty-cart checkout | Passed; no order saved |
| Sold-out item and quantity above stock | Passed |
| Zero, negative, decimal, huge, nonnumeric quantities | Passed; invalid additions rejected; zero update removes |
| Missing/invalid item fields and removal | Passed; friendly feedback, no crash |
| Per-item limit and accumulated additions | Passed; maximum 10 |
| Budget exceeded, malformed budget, exact budget | Passed |
| Pickup versus delivery | Passed; $4.91 pickup, $8.90 delivery for one Latte |
| Valid/invalid discount | Passed; discounted delivery Latte is $8.41 |
| Instructions and fulfillment validation | Passed; instructions saved, >300 characters rejected |
| Stock rechecked after another customer purchases | Passed |
| Stock decreases and survives restart | Passed; a fresh Python process reads saved stock and orders |
| Receipt refresh | Passed; unchanged receipt, no additional order |
| Report date/category filters and sorting | Passed; tested distinct quantity/revenue rankings, inclusive dates, invalid dates |
| Every main navigation destination and static asset | Passed; all return 200 |
| Unknown help question | Passed; useful fallback; known-topic response also checked |
| Settings preview and rendered checkout actions | Passed |
| Storage write failure | Passed; cart retained and stock unchanged |

During verification, a shared endpoint name could select the preview URL for the checkout form. It was corrected by giving the settings route its own endpoint name. The final tests explicitly verify both rendered form destinations. The first test run also emitted unclosed static-response warnings; tests now close those responses and the final run has no warnings.

No browser screenshot or visual layout inspection was performed. HTTP tests verify routes, rendered content, and business outcomes; students should rehearse on the presentation computer and check narrow-screen appearance. The app is designed for one local server process; concurrent multi-worker storage is outside its documented scope.
