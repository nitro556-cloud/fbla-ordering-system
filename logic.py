from data import menu

def search_menu(query):
    query = query.strip().lower()
    if query == "":
        return menu
    results = []
    for item in menu:
        if query in item["name"].lower() or query in item["category"].lower():
           results.append(item) 
    return results

def get_cart_items(cart):
    cart_items = []
    for item in menu:
        quantity = cart.get(str(item["id"]), 0)
        if quantity > 0:
            cart_items.append({**item, "quantity": quantity})
    return cart_items


def calculate_total(cart_items):
    return round(sum(item["price"] * item["quantity"] for item in cart_items), 2)