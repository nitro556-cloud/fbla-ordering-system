# Rendezvous Cafe

A Python + Flask + Jinja local-business digital ordering demonstration for FBLA Introduction to Programming, 2026–27. Plain CSS supplies the existing cafe appearance. No JavaScript or online service is needed. The concept is set in Cumming, Georgia; this is a simulation, with no payments or real fulfillment.

## Install and run

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create an environment: `python3 -m venv .venv` (Windows: `py -m venv .venv`).
4. Activate it: macOS/Linux `source .venv/bin/activate`; Windows `.venv\Scripts\activate`.
5. Install the only direct dependency: `python -m pip install -r requirements.txt`. This setup step needs internet unless Flask is already installed or supplied offline.
6. Run `python app.py`.
7. Visit `http://127.0.0.1:5001`. After installation the program works offline. Stop with Ctrl+C.

Optional: set environment variable `CAFE_SECRET_KEY` to a private random string before starting to keep signed browser carts valid across restarts. Otherwise a random temporary key is generated at launch; saved orders and stock still survive restarts. Debug mode is off.

## Features and topic mapping

- Browse and search lists of product dictionaries by name/category. Sold-out labels and available stock explain limits.
- Manage session cart quantities (1–10 each; update to 0 or remove). Server checks both whole-number format and meaningful limits even if browser checks are bypassed.
- Save pickup/delivery settings, a 300-character instructions note, optional budget, and CAFE10 discount. Saving updates the preview; checkout uses the form's current values.
- Integer cents avoid floating-point money errors. CAFE10 subtracts 10% of subtotal, then 7% demonstration tax applies to discounted items. Delivery adds 399 cents after tax. Percentage results round half a cent upward. These are project rules, not a claim about Georgia tax law.
- Checkout checks stock again, blocks overspending, subtracts inventory, and stores one JSON snapshot containing order details and stock. POST redirects to a numbered receipt so refresh cannot submit a purchase.
- Sales Report filters inclusive dates and category, sorts item sales by gross revenue or quantity, identifies the best seller by quantity, and lists current stock of 5 or fewer.
- Category filtering selects matching orders. Summary revenue is their complete checkout totals. Item revenue covers only matching items, before discount/tax/fees; labels explain this distinction.
- Help & Contact contains instructions, the event-topic explanation, and offline FAQ keyword matching with a helpful fallback. Our Story explains the student concept without invented business claims.

## Project structure

- `app.py`: Flask routes, forms, session access, template responses.
- `logic.py`: validation, search, quantities, cents totals, checkout, report analysis, FAQ rules.
- `data.py`: starting menu dictionaries and JSON read/write functions.
- `templates/base.html`: shared navigation and feedback; other templates supply page content. `_totals.html` shares cost labels.
- `static/`: existing CSS/photos plus `features.css` for new controls. Font imports removed for offline operation; system serif/sans-serif fonts are used.
- `script.js`: intentionally unused explanatory comment; no broken script request.
- `cafe_data.json`: created on the first successful order, never required for first launch. Keep this file to preserve sales and inventory. Back it up before changing it. Invalid JSON raises an error instead of silently resetting history.
- `test_app.py`: standard-library unittest + Flask test client; isolated temporary data.
- `DEMO_NOTES.md`, `AI_Use.md`, `TEST_RESULTS.md`: presentation preparation, disclosure, validation evidence.
- `COMPLETE_UPDATED_FILES.md`: complete review copies of changed source/documentation files, organized by batch.

Run tests with `python -m unittest -v test_app`. Tests never consume real demo stock. To deliberately reset the demonstration, stop the app and move `cafe_data.json` to a backup location before restarting.

## Libraries, Templates & Credits

- Flask 3.1.2: https://flask.palletsprojects.com/ (BSD-3-Clause), only direct dependency.
- Flask's installed dependencies: Werkzeug (HTTP utilities), Jinja2 (templates), MarkupSafe (escaping), itsdangerous (signed sessions), Click (CLI), Blinker (signals). Their versions are resolved by Flask's package metadata; see `python -m pip freeze` for the installed set. Standard Python modules include json, pathlib, datetime, re, os, secrets, tempfile, and unittest.
- Existing project HTML/CSS, cafe identity, and photos were supplied by the students' repository. Templates were revised with AI assistance; see AI_Use.md. No external HTML template was added.
- **STUDENTS MUST COMPLETE BEFORE SUBMISSION:** identify creator/source URL/license or permission for `logo.png`, `hero-image.png`, `homepage.jpg`, and each of the nine product photos in `static/images/`. Identify any original CSS/tutorial/template sources. No image ownership or license has been verified.
- Original CSS named Fraunces, Inter, and Montserrat through Google Fonts. The revised theme uses Georgia/Times for headings and system sans-serif fonts for text. No external font requests or font files are bundled. If font files are later added, record their source and license here.

## Known limitations

Single-process local classroom demo only: JSON storage has no multi-worker locking or database transactions. Run one server; simultaneous checkout is outside the supported demo. Reports and numbered receipts have no authentication and are visible to anyone who can access the local server. There is no CSRF protection, payment gateway, address collection, delivery dispatch, refund/cancellation flow, or inventory restocking screen. Delivery is a fee simulation only. Do not enter real personal information. Budget and checkout validation are server-side; settings must be saved to preview changed totals. The FAQ matches exact words, not generative AI. Timestamp uses the computer's local time; dates in reports use that same clock. Inventory and price administration require editing data while stopped. This implementation does not guarantee an FBLA score; students should confirm official event requirements and complete asset credits.
