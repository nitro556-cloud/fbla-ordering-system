# AI assistance disclosure

Session date: November 6, 2026. Students should review this log and add their names, verification notes, and any additional AI use before submission.

The assistant read the supplied request and existing Python, HTML, and CSS. It wrote or revised:

1. `app.py`: navigation routes, safe form handling, settings/checkout POST routes, persistent receipts, help, and report responses.
2. `logic.py`: integer-cents arithmetic, quantity/stock/budget/discount validation, saved order creation, report filters and sorting, and offline FAQ matching.
3. `data.py`: converted existing menu prices to integer cents and added JSON persistence with temporary-file replacement.
4. Templates: shared base navigation and totals partial; updated homepage/menu/cart/receipt; added help, story, and report pages.
5. Styling: retained original cafe CSS/images, removed online font imports for offline use, and added small shared styles. Images were not generated or researched.
6. Documentation: README, requirements, gitignore, this disclosure, demo notes, test results, and complete-file review document.
7. Verification: standard-library tests using Flask's test client and isolated JSON storage, including edge cases and persistence checks.

The assistant installed Flask 3.1.2 into a local virtual environment for verification. Flask was already the project's intended dependency; no new application libraries were introduced.

The assistant did not verify image/font ownership, official judging rules, or a real cafe's address/contact information. It removed invented pickup-location claims. Credits requiring student research are explicitly marked in README.

Students must read the code, explain its functions and limitations in their own words, and accurately disclose assistance under their competition's rules. Do not describe this code as entirely student-written.

## Follow-up styling revision

At the students’ request, AI consolidated overlapping CSS into shared theme and form styles, chose offline Georgia/system fonts, standardized spacing and buttons, simplified responsive menu/cart layouts, connected the receipt stylesheet, and added current-page navigation styling. The existing color palette and images were retained. All 12 test groups passed again; no browser visual inspection was available.
