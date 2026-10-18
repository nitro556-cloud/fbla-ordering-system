from flask import Flask, render_template, request, redirect, flash, session
from data import menu
from logic import search_menu, get_cart_items, calculate_total

app = Flask(__name__)
app.secret_key = "fbla-demo"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu_page():
    query = request.args.get("q","")
    return render_template("menu.html", menu = search_menu(query), query=query)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    item_id = int(request.form["item_id"])
    cart = session.get("cart", {})
    item_id = str(item_id)
    cart[item_id] = cart.get(item_id, 0) + 1
    session["cart"] = cart
    return redirect("/menu")

@app.route("/cart")
def cart_page():
    cart = session.get("cart", {})
    cart_items = get_cart_items(cart)
    subtotal, tax, total = calculate_total(cart_items)
    return render_template("cart.html", cart_items=cart_items,subtotal=subtotal,tax=tax, total=total)


@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    item_id = request.form["item_id"]
    cart = session.get("cart", {})
    cart.pop(item_id, None)
    session["cart"] = cart
    return redirect("/cart")

@app.route("/update-cart", methods=["POST"])
def update_cart():
    item_id = request.form["item_id"]
    quantity = int(request.form["quantity"])
    cart = session.get("cart", {})

    if quantity <= 0:
        cart.pop(item_id, None)
    else:
        cart[item_id] = quantity

    session["cart"] = cart
    return redirect("/cart")

@app.route("/receipt")
def receipt_page():
    cart = session.get("cart", {})
    cart_items = get_cart_items(cart)
    subtotal,tax,total = calculate_total(cart_items)
    session["cart"] = {}
    return render_template("receipt.html", cart_items=cart_items,subtotal=subtotal, tax=tax, total=total)


#Help and Contact Page
@app.route("/contact")
def contact_page():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)