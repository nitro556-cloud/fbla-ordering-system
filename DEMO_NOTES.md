# Seven-minute demonstration

Practice against the final app. Use a fresh backed-up demo data file so Croissant begins with 2 available. Two students can alternate at the marked times. Actual presentation quality and rule compliance remain the students' responsibility.

- **0:00–0:40, Student 1:** Introduce the local cafe ordering problem. Show Home and explain that Python/Flask handles the program, Jinja builds pages, and CSS supplies the appearance.
- **0:40–1:30, Student 1:** Open Help & Contact. Show the topic explanation and instructions. Ask about budget, then an unknown question to demonstrate the offline interactive feature and fallback. Point out consistent navigation.
- **1:30–2:20, Student 1:** Search Drinks, then Food. Show Cold Brew sold out and Croissant's limited stock. Add two Croissants. Explain browser quantity limits and Python's second check.
- **2:20–3:10, Student 2:** Open Your Order, change quantities and demonstrate removal. Add a Latte. Enter CAFE10 and a short instruction; save settings. Explain subtotal, discount, tax, and integer cents.
- **3:10–4:00, Student 2:** Select delivery, save, and show the $3.99 fee. Set a $1 budget and attempt checkout; show the block and removal/pickup suggestions. Raise the budget sufficiently and save.
- **4:00–4:50, Student 2:** Place an order. Show number, time, instructions, fulfillment and totals. Refresh to show the same receipt. Return to Menu and show decreased Croissant stock.
- **4:50–5:45, Student 1:** Show Sales Report. Apply today's date, a category filter, and quantity/revenue sorting. Explain gross item sales versus full-order revenue and point out current low stock.
- **5:45–6:30, Student 2:** Show app.py, logic.py, and data.py. Trace a short request from route to validation to JSON saving. Point to a loop, conditional, function, list, dictionary, and named variable.
- **6:30–7:00, Both:** Show test results, README setup/credits, and AI disclosure. State that this is an offline demonstration with no real payment or deliveries, and identify one future improvement: a database for concurrent orders.

## Fifteen likely judge questions

1. **Why three Python files?** Routes handle web requests, logic handles decisions and calculations, and data handles the menu and saved file.

2. **Why store cents?** 459 means $4.59. Integer arithmetic avoids binary floating-point rounding surprises.

3. **How do you calculate tax?** We apply 7% to the discounted subtotal and round half a cent upward using integer division.

4. **What data structures do you use?** Menu and orders are lists of dictionaries. The cart dictionary maps item ID strings to whole-number quantities.

5. **Where is a loop?** We loop over menu items when searching and over ordered items when subtracting stock.

6. **Where is a conditional?** Checkout checks whether the total exceeds the budget and returns an error if it does.

7. **Why validate on the server?** A person can bypass HTML restrictions. Python checks format, limits, current inventory, and budget again.

8. **What happens if stock changes?** Checkout reloads saved inventory and refuses the order if any requested quantity is unavailable.

9. **Why does refreshing a receipt work?** POST saves the order once, then redirects to a GET URL that only reads that order.

10. **Does data survive restart?** Orders and inventory are saved together in cafe_data.json. Session carts survive only if the secret key stays the same.

11. **How does the help box work?** It lowercases the question, extracts words, then checks keyword lists in order. Unknown words produce topic suggestions.

12. **How does the discount work?** CAFE10 selects 10 from a dictionary of percentages. It discounts items before tax and does not discount delivery.

13. **What does the category report mean?** It selects orders containing that category. Summary totals cover whole orders; item sales show only matching items.

14. **What are the limitations?** It is a one-server local demo. A real business needs authentication, a transactional database, CSRF protection, and payment and delivery systems.

15. **How was AI used?** AI revised the code and documentation and wrote tests. Our disclosure lists the changes; we must understand and verify them before presenting.
