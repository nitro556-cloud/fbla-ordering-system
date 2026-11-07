"""Beginner-readable validation, cents arithmetic, ordering, reports, and FAQ rules."""
from datetime import date, datetime
import re
from data import load_data, save_data

DISCOUNTS = {"CAFE10": 10}
FAQ = [
    (["budget", "limit", "afford"], "Set an optional budget in Your Order, then save settings. Checkout blocks totals above it. Remove an item, reduce quantities, or choose pickup."),
    (["delivery", "pickup", "fee"], "Pickup is free. Demo delivery adds $3.99. Select fulfillment and save settings before checkout. No real deliveries are dispatched."),
    (["stock", "sold", "available"], "Sold-out items cannot be added. The limit is 10 per item and checkout checks current stock again."),
    (["discount", "code", "coupon"], "Use CAFE10 for 10% off the items subtotal, before tax. Delivery is not discounted."),
    (["receipt", "order", "history"], "Checkout saves an order number and receipt. Sales Report lists past orders; refreshing a receipt never places another order."),
    (["allergy", "instructions"], "Save up to 300 characters of instructions in Your Order. This is a demonstration; confirm allergies directly with a real cafe."),
]


def money(cents):
    """Format integer cents as a dollar string for templates; return text."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def find_item(menu, item_id):
    """Find an item by its submitted ID in a menu list; return item or None."""
    for item in menu:
        if str(item["id"]) == str(item_id):
            return item
    return None


def search_menu(menu, query):
    """Search menu names and categories using text; return matching items."""
    results = []
    for item in menu:
        if query.strip().lower() in (item["name"] + " " + item["category"]).lower():
            results.append(item)
    return results


def change_quantity(cart, menu, item_id, quantity_text, adding=False):
    """Validate a submitted quantity and change cart; return an error or None."""
    item = find_item(menu, item_id)
    if item is None:
        return "Choose an existing menu item."
    # Check length before int() so extremely long user input is harmless.
    if not re.fullmatch(r"[0-9]{1,2}", quantity_text):
        return "Quantity must be a whole number from 1 to 10 (0 removes an item when updating)."
    quantity = int(quantity_text)
    key = str(item["id"])
    if adding:
        if quantity == 0:
            return "Add at least 1 item."
        quantity += cart.get(key, 0)
    if quantity > 10:
        return "The limit is 10 per item."
    if quantity == 0:
        cart.pop(key, None)
        return None
    if item["stock"] == 0:
        return item["name"] + " is sold out."
    if quantity > item["stock"]:
        return "Only " + str(item["stock"]) + " " + item["name"] + " left."
    cart[key] = quantity
    return None


def get_cart_items(cart, menu):
    """Join session quantities to menu data; return independent item dictionaries."""
    items = []
    for item in menu:
        quantity = cart.get(str(item["id"]), 0)
        if quantity > 0:
            entry = dict(item)
            entry["quantity"] = quantity
            items.append(entry)
    return items


def parse_settings(form):
    """Validate checkout settings from a form; return settings and an error."""
    fulfillment = form.get("fulfillment", "pickup")
    instructions = form.get("instructions", "").strip()
    code = form.get("discount_code", "").strip().upper()
    budget_text = form.get("budget", "").strip()
    settings = {"fulfillment": fulfillment, "instructions": instructions,
                "discount_code": code, "budget_text": budget_text, "budget": None}
    if fulfillment not in ("pickup", "delivery"):
        return settings, "Choose pickup or delivery."
    if len(instructions) > 300:
        return settings, "Instructions must be 300 characters or fewer."
    if code and code not in DISCOUNTS:
        return settings, "Unknown discount code. Use CAFE10 or leave it blank."
    if budget_text:
        if not re.fullmatch(r"[0-9]{1,6}(\.[0-9]{1,2})?", budget_text):
            return settings, "Budget must be a nonnegative dollar amount with at most two decimals."
        parts = budget_text.split(".")
        cents = int(parts[0]) * 100
        if len(parts) == 2:
            cents += int(parts[1].ljust(2, "0"))
        settings["budget"] = cents
    return settings, None


def calculate_total(items, settings):
    """Calculate item subtotal, discount, 7% tax, fee, and total in cents."""
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]
    percent = DISCOUNTS.get(settings.get("discount_code", ""), 0)
    # Add 50 before integer division to round half a cent upward.
    discount = (subtotal * percent + 50) // 100
    tax = ((subtotal - discount) * 7 + 50) // 100
    delivery_fee = 399 if settings.get("fulfillment") == "delivery" else 0
    return {"subtotal": subtotal, "discount": discount, "tax": tax,
            "delivery_fee": delivery_fee, "total": subtotal - discount + tax + delivery_fee}


def place_order(cart, settings):
    """Recheck cart and budget, persist stock and order; return order and error."""
    state = load_data()
    if not cart:
        return None, "Your cart is empty. Add an item before checkout."
    for item_id, quantity in cart.items():
        item = find_item(state["menu"], item_id)
        if item is None or type(quantity) is not int or quantity < 1 or quantity > 10:
            return None, "Your cart contains an invalid item or quantity. Please update it."
        if quantity > item["stock"]:
            return None, item["name"] + " no longer has enough stock. Reduce or remove it."
    items = get_cart_items(cart, state["menu"])
    totals = calculate_total(items, settings)
    if settings["budget"] is not None and totals["total"] > settings["budget"]:
        return None, "Budget exceeded. Reduce quantities, remove an item, or choose pickup."
    order = {"number": len(state["orders"]) + 1,
             "timestamp": datetime.now().isoformat(timespec="seconds"),
             "items": items, **totals, **settings}
    for item in items:
        find_item(state["menu"], item["id"])["stock"] -= item["quantity"]
    state["orders"].append(order)
    try:
        save_data(state)
    except OSError:
        return None, "Could not save the order. Your cart is unchanged; please try again."
    return order, None


def answer_question(question):
    """Match question words to offline FAQ topics; return an answer string."""
    words = re.findall(r"[a-z]+", question.lower())
    for keywords, answer in FAQ:
        for keyword in keywords:
            if keyword in words:
                return answer
    return "Try asking about budget, delivery, stock, discount codes, receipts, or instructions. You can also read the steps below."


def build_report(orders, menu, filters):
    """Filter orders by date/category and sort item sales; return report data/error."""
    start = filters.get("start", "")
    end = filters.get("end", "")
    category = filters.get("category", "")
    sort = filters.get("sort", "revenue")
    try:
        if start:
            date.fromisoformat(start)
        if end:
            date.fromisoformat(end)
    except ValueError:
        return None, "Use valid dates in YYYY-MM-DD format."
    if start and end and start > end:
        return None, "Start date must be on or before end date."
    if category not in ("", "Drinks", "Food") or sort not in ("revenue", "quantity"):
        return None, "Choose a listed category and sort option."
    selected = []
    sales = {}
    revenue = 0
    for order in orders:
        day = order["timestamp"][:10]
        if (start and day < start) or (end and day > end):
            continue
        matching = []
        for item in order["items"]:
            if category and item["category"] != category:
                continue
            matching.append(item)
            row = sales.setdefault(item["name"], {"name": item["name"], "quantity": 0, "revenue": 0})
            row["quantity"] += item["quantity"]
            row["revenue"] += item["price"] * item["quantity"]
        if matching:
            selected.append(order)
            revenue += order["total"]
    rows = list(sales.values())
    if sort == "quantity":
        rows.sort(key=sales_quantity, reverse=True)
    else:
        rows.sort(key=sales_revenue, reverse=True)
    best = None
    if rows:
        best = max(rows, key=sales_quantity)
    low_stock = []
    for item in menu:
        if item["stock"] <= 5 and (not category or item["category"] == category):
            low_stock.append(item)
    return {"orders": selected, "revenue": revenue, "sales": rows,
            "best": best, "low_stock": low_stock}, None


def sales_quantity(row):
    """Read a sales row dictionary and return its quantity for sorting."""
    return row["quantity"]


def sales_revenue(row):
    """Read a sales row dictionary and return its gross cents for sorting."""
    return row["revenue"]
