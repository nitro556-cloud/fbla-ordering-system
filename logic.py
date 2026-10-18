from data import menu

tax_rate = 0.07

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
    subtotal = round(sum(item["price"] * item["quantity"] for item in cart_items), 2)
    tax = round(subtotal * tax_rate,2)
    total = round(subtotal + tax,2)
    return subtotal, tax, total



def find_item(item_id_text):
    if not str(item_id_text).isdigit():
        return None
    for item in menu:
        if item["id"] == int(item_id_text):
            return item
    return None



def add_item(cart, item_id_text, quantity_text):
    if not quantity_text.isdigit() or int(quantity_text) < 1:
        return "Quantity must be a whole number of 1 or more."
    item = find_item(item_id_text)
    if item is None:
        return "That item doesn't exist."
    if item["stock"] == 0:
        return item["name"] + " is sold out."
    key = str(item["id"])
    new_quantity = cart.get(key, 0) + int(quantity_text)
    if new_quantity > item["stock"]:
        return "Only " + str(item["stock"]) + " " + item["name"] + " available."
    cart[key] = new_quantity
    return None


def update_item(cart, item_id_text, quantity_text):
    if not quantity_text.isdigit():
        return "Quantity must be a whole number."
    item = find_item(item_id_text)
    if item is None:
        return "That item doesn't exist."
    key = str(item["id"])
    quantity = int(quantity_text)
    if quantity == 0:
        cart.pop(key, None)
    elif quantity > item["stock"]:
        return "Only " + str(item["stock"]) + " " + item["name"] + " available."
    else:
        cart[key] = quantity
    return None
