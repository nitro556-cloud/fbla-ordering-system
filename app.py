"""Flask routes connect browser forms to the cafe's business logic and templates."""
import os
import secrets
from flask import Flask, render_template, request, redirect, flash, session, url_for, abort
from data import load_data
from logic import (money, search_menu, change_quantity, get_cart_items,
                   parse_settings, calculate_total, place_order, answer_question, build_report)

app = Flask(__name__)
# An environment key keeps carts across restarts; a random demo key avoids a public secret.
app.secret_key = os.environ.get("CAFE_SECRET_KEY") or secrets.token_hex(32)
app.config["MAX_CONTENT_LENGTH"] = 16384
app.jinja_env.filters["money"] = money


@app.route("/")
def home():
    """Render the homepage; take no form input and return HTML."""
    return render_template("index.html")


@app.route("/menu")
def menu_page():
    """Read a search query and return matching menu cards."""
    query = request.args.get("q", "")
    return render_template("menu.html", menu=search_menu(load_data()["menu"], query), query=query)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    """Validate item/quantity input, update session cart, and redirect to menu."""
    cart = session.get("cart", {})
    error = change_quantity(cart, load_data()["menu"], request.form.get("item_id", ""),
                            request.form.get("quantity", ""), adding=True)
    session["cart"] = cart
    flash(error or "Added to your cart!")
    return redirect(url_for("menu_page"))


@app.route("/cart")
def cart_page():
    """Read cart and saved settings; return item rows and a cost preview."""
    settings = session.get("settings") or parse_settings({})[0]
    items = get_cart_items(session.get("cart", {}), load_data()["menu"])
    return render_template("cart.html", cart_items=items, settings=settings,
                           totals=calculate_total(items, settings))


@app.route("/update-cart", methods=["POST"])
def update_cart():
    """Validate an item's replacement quantity and redirect to the cart."""
    cart = session.get("cart", {})
    error = change_quantity(cart, load_data()["menu"], request.form.get("item_id", ""),
                            request.form.get("quantity", ""))
    session["cart"] = cart
    flash(error or "Quantity updated.")
    return redirect(url_for("cart_page"))


@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    """Remove an existing submitted cart ID safely; redirect with feedback."""
    cart = session.get("cart", {})
    item_id = request.form.get("item_id", "")
    if item_id in cart:
        cart.pop(item_id)
        flash("Item removed.")
    else:
        flash("Choose an item in your cart to remove.")
    session["cart"] = cart
    return redirect(url_for("cart_page"))


@app.route("/checkout", methods=["POST"])
@app.route("/cart-settings", methods=["POST"], endpoint="save_settings")
def checkout():
    """Validate settings; save preview settings or place an order and redirect."""
    settings, error = parse_settings(request.form)
    if error:
        flash(error)
        return render_template("cart.html", cart_items=get_cart_items(session.get("cart", {}), load_data()["menu"]),
                               settings=settings, totals=None), 400
    session["settings"] = settings
    if request.path == "/cart-settings":
        flash("Settings saved. Review your updated total below.")
        return redirect(url_for("cart_page"))
    order, error = place_order(session.get("cart", {}), settings)
    if error:
        flash(error)
        return redirect(url_for("cart_page"))
    session["cart"] = {}
    session.pop("settings", None)
    return redirect(url_for("receipt_page", number=order["number"]))


@app.route("/receipt/<int:number>")
def receipt_page(number):
    """Look up a saved order number and return a refresh-safe receipt or 404."""
    for order in load_data()["orders"]:
        if order["number"] == number:
            return render_template("receipt.html", order=order)
    abort(404)


@app.route("/receipt")
def old_receipt():
    """Redirect the legacy receipt URL to the report without changing data."""
    return redirect(url_for("report_page"))


@app.route("/report")
def report_page():
    """Read report filters and return sales summaries or a friendly input error."""
    state = load_data()
    report, error = build_report(state["orders"], state["menu"], request.args)
    return render_template("report.html", report=report, error=error, filters=request.args), 400 if error else 200


@app.route("/help", methods=["GET", "POST"])
@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    """Read an optional FAQ question and return help, instructions, and contact context."""
    question = request.form.get("question", "")[:300]
    answer = answer_question(question) if request.method == "POST" else ""
    return render_template("contact.html", question=question, answer=answer)


@app.route("/story")
def story_page():
    """Return the student project's story page without form inputs."""
    return render_template("story.html")


if __name__ == "__main__":
    app.run(debug=False, port=5001)
