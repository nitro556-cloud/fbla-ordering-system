# Complete updated files

Full review copies of every changed or added source and documentation file, one file at a time. This generated document is excluded from its own contents. The actual project files are ready to run.

## Batch 1 — Web pages and working controls

### templates/base.html

````html
{# Shared page structure keeps navigation and feedback identical across pages. #}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rendezvous Cafe | {% block title %}Ordering{% endblock %}
</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='menu-style.css') }}">
{% block styles %}
{% endblock %}
<link rel="stylesheet" href="{{ url_for('static', filename='features.css') }}">
</head>
<body>
<header>
<a href="{{ url_for('home') }}">
<img id="logo" src="{{ url_for('static', filename='images/logo.png') }}" alt="Rendezvous Cafe home">
</a>
<nav id="navigation_bar" aria-label="Main navigation">
<ul>
{% for endpoint, label in [('home','Home'), ('menu_page','Menu'), ('cart_page','Your Order'), ('report_page','Sales Report'), ('story_page','Our Story'), ('contact_page','Help & Contact')] %}
<li>
<a href="{{ url_for(endpoint) }}" {% if request.endpoint == endpoint %}aria-current="page"{% endif %}>{{ label }}</a>
</li>
{% endfor %}
</ul>
</nav>
</header>
<div class="feedback" aria-live="polite">
{% for message in get_flashed_messages() %}
<p>{{ message }}</p>
{% endfor %}
</div>
{% block content %}
{% endblock %}
<footer>Student ordering demonstration · Cumming, Georgia · No payments or real deliveries</footer>
</body>
</html>

````

### templates/index.html

````html
{# Homepage introduces the cafe and links directly to ordering. #}
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}
    <main>
        <!-- Hero section -->
        <section class="hero-section">
            <div class="section-content">
                <div class="hero-details">
                    <h2 class="title">Best Coffee</h2>
                    <h3 class="subtitle">Make your day great with our special coffee!</h3>
                    <p class="description">Enjoy some delicious food in a nice atmosphere and some romance with your favorite meal. We invite you to come hungry and leave us satisfied with our delicious menu.</p>
                    <a href="/menu" class="order-now-btn">Order Now</a>
                </div>
                <div class="hero-image-holder">
                    <img src="{{ url_for('static', filename='./images/hero-image.png') }}" alt="Coffee Image" class="hero-image">
                </div>
            </div>
        </section>
    </main>

{% endblock %}

````

### templates/menu.html

````html
{# Menu cards show prices, available inventory, and quantity forms. #}
{% extends "base.html" %}
{% block title %}Menu{% endblock %}
{% block content %}
<section>
<h1 class="page-title">Our Menu</h1>
<p>Choose 1–10 of each item, within available stock. Review totals in Your Order.</p>
</section>
<section>
<form method="get">
<label for="search">Search menu</label>
<input id="search" name="q" value="{{ query }}" type="text">
<button>Search</button>
</form>
<nav aria-label="Menu categories">
{% for category in ['', 'Drinks', 'Food'] %}
<a href="{{ url_for('menu_page', q=category) }}">{{ category or 'All Items' }}</a>
{% endfor %}
</nav>
</section>
<section class="menu-grid">
{% for item in menu %}
<article class="menu-item">
<img class="menu-item-img" src="{{ url_for('static', filename='images/' ~ item.image) }}" alt="{{ item.name }}">
<div class="menu-item-content">
<h2>{{ item.name }}</h2>
<p>{{ item.category }} · {{ item.price|money }}</p>
<p>
{% if item.stock == 0 %}Sold Out{% else %}Only {{ item.stock }} left{% endif %}
</p>
<form action="{{ url_for('add_to_cart') }}" method="post">
<input type="hidden" name="item_id" value="{{ item.id }}">
<label for="qty-{{ item.id }}">Quantity</label>
<input id="qty-{{ item.id }}" name="quantity" type="number" min="1" max="{{ [10, item.stock]|min }}" value="1" required {% if not item.stock %}disabled{% endif %}>
<button {% if not item.stock %}disabled{% endif %}>Add to Cart</button>
</form>
</div>
</article>
{% else %}
<p>No items found. Try another search.</p>
{% endfor %}
</section>
{% endblock %}

````

### templates/cart.html

````html
{# Cart item forms and checkout settings submit actual values to Flask. #}
{% extends "base.html" %}
{% block title %}Your Order{% endblock %}
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='cart-style.css') }}">
{% endblock %}
{% block content %}
<section>
<h1 class="page-title">Your Order</h1>
<p>Update quantities (0 removes), then save settings to preview the total. Checkout uses the settings currently entered.</p>
</section>
<main class="cart-container">
<section class="order-summary-card">
{% for item in cart_items %}
<div class="cart-item-row">
<img width="80" src="{{ url_for('static', filename='images/' ~ item.image) }}" alt="{{ item.name }}">
<div>
<h2>{{ item.name }}</h2>
<p>{{ (item.price * item.quantity)|money }} · {{ item.stock }} available</p>
<form action="{{ url_for('update_cart') }}" method="post">
<input type="hidden" name="item_id" value="{{ item.id }}">
<label for="qty-{{ item.id }}">Quantity</label>
<input id="qty-{{ item.id }}" name="quantity" type="number" min="0" max="10" value="{{ item.quantity }}" required>
<button>Update</button>
</form>
<form class="remove-form" action="{{ url_for('remove_from_cart') }}" method="post">
<input type="hidden" name="item_id" value="{{ item.id }}">
<button>Remove</button>
</form>
</div>
</div>
{% else %}
<h2>Your cart is empty</h2>
<a href="{{ url_for('menu_page') }}">Browse Menu</a>
{% endfor %}
</section>
<section class="info-card">
<form class="settings-form" action="{{ url_for('checkout') }}" method="post">
<fieldset>
<legend>Fulfillment</legend>
{% for option in ['pickup', 'delivery'] %}
<label>
<input type="radio" name="fulfillment" value="{{ option }}" {% if settings.fulfillment == option %}checked{% endif %}>{{ option|title }} {% if option == 'delivery' %}($3.99 demo fee){% else %}(free){% endif %}
</label>
{% endfor %}
</fieldset>
<label for="instructions">Special instructions (up to 300 characters)</label>
<textarea id="instructions" name="instructions" maxlength="300">{{ settings.instructions }}</textarea>
<label for="discount">Discount code (CAFE10 saves 10% on items)</label>
<input id="discount" name="discount_code" value="{{ settings.discount_code }}" type="text">
<label for="budget">Optional budget in dollars (leave blank for no limit)</label>
<input id="budget" name="budget" value="{{ settings.budget_text }}" inputmode="decimal" type="text">
<button formaction="{{ url_for('save_settings') }}">Save settings & preview total</button>
{% if totals %}
{% include '_totals.html' %}
{% if settings.budget is not none %}
<p>Budget remaining: {{ (settings.budget - totals.total)|money }}</p>
{% if totals.total > settings.budget %}
<p role="alert">Budget exceeded. Reduce quantities, remove an item, or choose pickup. Checkout will block this order.</p>
{% endif %}
{% endif %}
{% else %}
<p>Fix the settings above to calculate your total.</p>
{% endif %}
<button class="checkout-btn" {% if not cart_items %}disabled{% endif %}>Place order</button>
</form>
</section>
</main>
{% endblock %}

````

### templates/_totals.html

````html
{# Reuse identical money labels on the cart and saved receipt. #}
<dl class="totals-breakdown">
{% for key, label in [('subtotal','Subtotal'), ('discount','Discount (subtract)'), ('tax','Tax (7%)'), ('delivery_fee','Delivery fee'), ('total','Total')] %}
<div class="line-item">
<dt>{{ label }}</dt>
<dd>{{ totals[key]|money }}</dd>
</div>
{% endfor %}
</dl>

````

### templates/receipt.html

````html
{# A saved order snapshot makes receipt refresh safe and preserves old prices. #}
{% extends "base.html" %}
{% block title %}Receipt {{ order.number }}{% endblock %}
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='receipt-style.css') }}">
{% endblock %}
{% block content %}
<section class="receipt-card">
<h1>Order #{{ order.number }}</h1>
<p>{{ order.timestamp }} · {{ order.fulfillment|title }}</p>
{% for item in order['items'] %}
<p>{{ item.name }} × {{ item.quantity }} — {{ (item.price * item.quantity)|money }}</p>
{% endfor %}
{% set totals = order %}
{% include '_totals.html' %}
<p>Discount code: {{ order.discount_code or 'None' }}</p>
<p>Instructions: {{ order.instructions or 'None' }}</p>
<p>Order saved. You can refresh this receipt safely.</p>
<a href="{{ url_for('menu_page') }}">Back to Menu</a>
</section>
{% endblock %}

````

### templates/contact.html

````html
{# Instructions and keyword FAQ assistance work completely offline. #}
{% extends "base.html" %}
{% block title %}Help & Contact{% endblock %}
{% block content %}
<section>
<h1>Help & Contact</h1>
<h2>Ask an ordering question</h2>
<form method="post">
<label for="question">Your question</label>
<input type="text" id="question" name="question" maxlength="300" value="{{ question }}" placeholder="How does the budget work?">
<button>Ask</button>
</form>
{% if answer %}
<p role="status">{{ answer }}</p>
{% endif %}
<h2>How to use this program</h2>
<ol>
<li>Browse Menu; search by name or select Drinks or Food.</li>
<li>Choose a whole-number quantity up to 10 and available stock, then Add to Cart.</li>
<li>Open Your Order to update or remove items.</li>
<li>Select fulfillment, add instructions, optionally enter CAFE10 and a budget, and save settings.</li>
<li>Review the total and place the order. Save the receipt number.</li>
<li>Open Sales Report to filter orders by date/category and compare item sales.</li>
</ol>
<h2>Local Business Digital Ordering System</h2>
<p>This student project lets cafe customers browse products, manage a cart, calculate costs, stay within a budget, and review saved orders. Inventory checks prevent selling unavailable products. Sales summaries help a local business understand demand.</p>
<h2>Contact</h2>
<p>Rendezvous Cafe is a student demonstration set in Cumming, Georgia. Real contact details and a verified pickup address have not been supplied. No real orders are sent.</p>
</section>
{% endblock %}

````

### templates/story.html

````html
{# Explain the project without inventing a real business history. #}
{% extends "base.html" %}
{% block title %}Our Story{% endblock %}
{% block content %}
<section>
<h1>Our Story</h1>
<p>Rendezvous Cafe is a student-built local business ordering demonstration for FBLA Introduction to Programming. Our goal is to make browsing food, managing quantities, and understanding purchase totals easy.</p>
<p>The cafe concept is set in Cumming, Georgia. This prototype does not accept payments or dispatch deliveries.</p>
<a href="{{ url_for('contact_page') }}">Read the ordering instructions</a>
</section>
{% endblock %}

````

### templates/report.html

````html
{# Date/category filters and item sorting help analyze saved order history. #}
{% extends "base.html" %}
{% block title %}Sales Report{% endblock %}
{% block content %}
<section>
<h1>Sales Report</h1>
<form method="get">
<label>From <input type="date" name="start" value="{{ filters.get('start','') }}">
</label>
<label>Through <input type="date" name="end" value="{{ filters.get('end','') }}">
</label>
<label>Category <select name="category">
{% for option in ['', 'Drinks', 'Food'] %}
<option value="{{ option }}" {% if filters.get('category','') == option %}selected{% endif %}>{{ option or 'All' }}</option>
{% endfor %}
</select>
</label>
<label>Sort items by <select name="sort">
{% for option in ['revenue','quantity'] %}
<option {% if filters.get('sort','revenue') == option %}selected{% endif %}>{{ option }}</option>
{% endfor %}
</select>
</label>
<button>Apply filters</button>
<a href="{{ url_for('report_page') }}">Reset</a>
</form>
{% if error %}
<p role="alert">{{ error }}</p>
{% else %}
<p>Matching orders: {{ report.orders|length }} · Full-order revenue: {{ report.revenue|money }}</p>
<p>Category filters select orders containing that category. Full-order revenue includes all their items, discounts, tax, and delivery. Item revenue below is before discounts/tax/fees and includes only the selected category.</p>
<p>Best seller by quantity: {% if report.best %}{{ report.best.name }} ({{ report.best.quantity }}){% else %}No sales yet{% endif %}
</p>
<table>
<caption>Item sales</caption>
<tr>
<th>Item</th>
<th>Quantity</th>
<th>Item revenue</th>
</tr>
{% for row in report.sales %}
<tr>
<td>{{ row.name }}</td>
<td>{{ row.quantity }}</td>
<td>{{ row.revenue|money }}</td>
</tr>
{% endfor %}
</table>
<h2>Order history</h2>
{% for order in report.orders %}
<p>
<a href="{{ url_for('receipt_page', number=order.number) }}">Order #{{ order.number }}</a> · {{ order.timestamp }} · {{ order.total|money }}</p>
{% else %}
<p>No matching orders.</p>
{% endfor %}
<h2>Current low stock (5 or fewer)</h2>
<p>Current inventory, independent of the date filter.</p>
{% for item in report.low_stock %}
<p>{{ item.name }}: {{ item.stock }}</p>
{% else %}
<p>No low-stock items.</p>
{% endfor %}
{% endif %}
</section>
{% endblock %}

````

### static/style.css

````css
/* Shared cafe theme: system fonts work offline on every presentation computer. */
:root {
    --background: #f7f2e9;
    --surface: #fffdf8;
    --ink: #2f4f4a;
    --muted: #66766f;
    --accent: #a66d42;
    --border: #d9dfd5;
    --radius: 16px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: var(--background);
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
h1, h2, h3, .title, .subtitle {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 500;
    line-height: 1.2;
    text-wrap: balance;
}
h1, .page-title { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 16px; }
h2 { font-size: 1.6rem; margin-bottom: 16px; }
h3 { font-size: 1.25rem; margin-bottom: 12px; }
p { margin-bottom: 16px; }
a { color: var(--ink); text-underline-offset: 4px; }
a:hover { color: var(--accent); }

/* All content shares one width instead of accumulating nested percentage padding. */
body > section, body > main, body > .feedback {
    width: min(1120px, calc(100% - 48px));
    margin-inline: auto;
}
body > section, body > main { margin-block: 36px; }
section { min-width: 0; }
header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 16px max(24px, calc((100% - 1120px) / 2));
    border-bottom: 1px solid var(--border);
}
header > a { display: flex; flex-shrink: 0; }
#logo { width: 76px; height: 76px; object-fit: contain; }
#navigation_bar ul { display: flex; flex-wrap: wrap; gap: 6px; list-style: none; }
#navigation_bar a {
    display: block;
    padding: 8px 12px;
    border-radius: 8px;
    text-decoration: none;
    font-size: .9rem;
    font-weight: 600;
}
#navigation_bar a:hover, #navigation_bar a[aria-current="page"] { background: #e7ece3; color: var(--ink); }
footer {
    max-width: 1120px;
    margin: 64px auto 0;
    padding: 24px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: .85rem;
    text-align: center;
}

/* A restrained two-column hero uses the same alignment as the other pages. */
.hero-section { padding: 24px 0; }
.hero-section .section-content { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: center; }
.title { font-size: clamp(2.75rem, 5vw, 4.5rem); margin-bottom: 20px; }
.subtitle { font-size: 1.6rem; color: var(--accent); }
.description { max-width: 48ch; margin: 24px 0 32px; color: var(--muted); }
.hero-image { display: block; width: 100%; height: 420px; object-fit: cover; border-radius: var(--radius); }

@media (max-width: 760px) {
    header { flex-direction: column; gap: 12px; padding: 16px; }
    #navigation_bar ul { justify-content: center; }
    #navigation_bar a { padding: 8px; }
    body > section, body > main, body > .feedback { width: calc(100% - 32px); }
    .hero-section .section-content { grid-template-columns: 1fr; gap: 32px; }
    .hero-image { height: 300px; }
    footer { margin-top: 40px; }
}

````

### static/menu-style.css

````css
/* Menu-specific styling; shared typography and controls live in style/features. */
nav[aria-label="Menu categories"] { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }
nav[aria-label="Menu categories"] a {
    padding: 8px 18px;
    border: 1px solid var(--border);
    border-radius: 24px;
    background: var(--surface);
    text-decoration: none;
    font-size: .9rem;
}
nav[aria-label="Menu categories"] a:hover { background: #e7ece3; }
.menu-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
.menu-item { display: flex; flex-direction: column; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; background: var(--surface); }
.menu-item-img { display: block; width: 100%; height: 220px; object-fit: cover; }
.menu-item-content { display: flex; flex: 1; flex-direction: column; padding: 24px; }
.menu-item-content h2 { font-size: 1.5rem; margin-bottom: 8px; }
.menu-item-content p { color: var(--muted); margin-bottom: 10px; font-size: .95rem; }
.menu-item-content form { margin-top: auto; padding-top: 12px; }
.menu-item-content button { flex: 1; }
.menu-item-img[alt="Croissant"] { object-position: center 70%; }
.menu-item-img[alt="Black Coffee"] { object-position: center 60%; }
@media (max-width: 950px) { .menu-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 600px) { .menu-grid { grid-template-columns: 1fr; } }

````

### static/cart-style.css

````css
/* Cart-specific layout. Shared controls and totals are defined in features.css. */
.cart-container { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 24px; align-items: start; }
.info-card, .order-summary-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 28px; }
.cart-item-row { display: flex; align-items: flex-start; gap: 20px; padding: 24px 0; border-bottom: 1px solid var(--border); }
.cart-item-row:first-child { padding-top: 0; }
.cart-item-row:last-child { padding-bottom: 0; border-bottom: 0; }
.cart-item-row > img { width: 80px; height: 80px; object-fit: cover; border-radius: 12px; flex-shrink: 0; }
.cart-item-row > div { min-width: 0; flex: 1; }
.cart-item-row h2 { font-size: 1.4rem; margin-bottom: 8px; }
.cart-item-row p { font-size: .9rem; color: var(--muted); }
.cart-item-row form { gap: 8px; }
.cart-item-row button { padding: 8px 12px; font-size: .85rem; }
.remove-form button { color: var(--muted); background: transparent; border-color: var(--border); }
.settings-form { display: flex; flex-direction: column; align-items: stretch; gap: 12px; margin: 0; }
.settings-form > label { margin-top: 8px; }
.settings-form input[type="text"] { max-width: none; width: 100%; }
.settings-form fieldset { margin-bottom: 8px; }
.settings-form button[formaction] { background: #e7ece3; color: var(--ink); border-color: var(--border); }
@media (max-width: 900px) { .cart-container { grid-template-columns: minmax(0, 1fr); } }
@media (max-width: 480px) {
    .info-card, .order-summary-card { padding: 20px; }
    .cart-item-row { gap: 12px; }
    .cart-item-row > img { width: 56px; height: 56px; }
}

````

### static/receipt-style.css

````css
/* The receipt uses the same card and totals treatment as checkout. */
body > .receipt-card {
    max-width: 680px;
    padding: clamp(24px, 5vw, 40px);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
}
.receipt-card > p { overflow-wrap: anywhere; }
.receipt-card > a { display: inline-block; margin-top: 16px; font-weight: 600; }

````

### static/features.css

````css
/* Consistent form controls, feedback, and reports shared by every page. */
form { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin: 16px 0; }
label, legend { font-size: .9rem; font-weight: 600; }
input, textarea, select, button { font: inherit; }
input:not([type="radio"]):not([type="hidden"]), textarea, select {
    min-width: 0;
    max-width: 100%;
    min-height: 44px;
    padding: 10px 12px;
    border: 1px solid #b9c6bd;
    border-radius: 8px;
    color: var(--ink);
    background: var(--surface);
}
input[type="text"] { flex: 1; max-width: 520px; }
input[type="number"] { width: 70px; }
textarea { width: 100%; min-height: 110px; resize: vertical; }
select { cursor: pointer; }
button, .order-now-btn, .checkout-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 44px;
    padding: 10px 20px;
    border: 1px solid var(--ink);
    border-radius: 8px;
    color: var(--surface);
    background: var(--ink);
    font-size: .95rem;
    font-weight: 600;
    line-height: 1.4;
    text-decoration: none;
    cursor: pointer;
    transition: background-color .15s ease;
}
button:hover, .order-now-btn:hover, .checkout-btn:hover { background: #3c625b; color: var(--surface); }
button:disabled { opacity: .45; cursor: not-allowed; }
:where(a, button, input, textarea, select):focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
fieldset { border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px; }
legend { padding: 0 6px; }
fieldset label { display: flex; align-items: center; gap: 10px; padding: 8px 0; font-weight: 400; }
input[type="radio"] { accent-color: var(--ink); width: 17px; height: 17px; }
.feedback:empty { display: none; }
.feedback p, [role="alert"], p[role="status"] { border: 1px solid #c7d5c8; background: #edf2e9; padding: 14px 18px; border-radius: 10px; margin-top: 16px; overflow-wrap: anywhere; }
[role="alert"] { background: #fcf0e5; border-color: #ddbea4; color: #784322; }
.totals-breakdown { border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 12px 0; margin: 16px 0; }
.line-item { display: flex; justify-content: space-between; align-items: baseline; gap: 16px; padding: 6px 0; font-size: .95rem; }
.line-item dd { white-space: nowrap; font-variant-numeric: tabular-nums; }
.line-item:last-child { font-size: 1.15rem; font-weight: 700; border-top: 1px solid var(--border); margin-top: 8px; padding-top: 14px; }
table { width: 100%; border-collapse: collapse; margin: 24px 0; font-variant-numeric: tabular-nums; background: var(--surface); }
caption { text-align: left; font-weight: 600; padding-bottom: 12px; }
th, td { text-align: left; padding: 12px 16px; border-bottom: 1px solid var(--border); }
th { background: #e7ece3; font-size: .9rem; }
ol { padding-left: 24px; }
li { margin-bottom: 6px; }
section > h2:not(:first-child) { margin-top: 32px; }
@media (max-width: 480px) {
    th, td { padding: 10px 8px; font-size: .85rem; }
    input[type="text"] { flex-basis: 100%; }
    .settings-form input[type="text"] { flex-basis: auto; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }

````

### script.js

````javascript
// No JavaScript is required. Flask handles all forms and offline FAQ matching.

````

**What changed and why:** Navigation and feedback are shared across pages. Forms now submit real quantities, fulfillment, instructions, discounts, and budgets. Existing photos and cafe styling remain; external font imports were removed so pages work offline.

## Batch 2 — Validated ordering, storage, and reports

### app.py

````python
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

````

### logic.py

````python
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

````

### data.py

````python
"""Menu data and JSON storage for the single-process, offline cafe demo."""
import json
import os
from pathlib import Path

MENU = [
    {'id': 1, 'name': 'Latte', 'category': 'Drinks', 'price': 459, 'stock': 50, 'image': 'latte.jpg'},
    {'id': 2, 'name': 'Espresso', 'category': 'Drinks', 'price': 359, 'stock': 75, 'image': 'espresso.jpg'},
    {'id': 3, 'name': 'Cold Brew', 'category': 'Drinks', 'price': 379, 'stock': 0, 'image': 'cold-brew.jpg'},
    {'id': 4, 'name': 'Iced Tea', 'category': 'Drinks', 'price': 299, 'stock': 20, 'image': 'iced-tea.jpg'},
    {'id': 5, 'name': 'Black Coffee', 'category': 'Drinks', 'price': 249, 'stock': 20, 'image': 'black-coffee.jpg'},
    {'id': 6, 'name': 'Blueberry Muffin', 'category': 'Food', 'price': 550, 'stock': 20, 'image': 'blueberry-muffin.jpg'},
    {'id': 7, 'name': 'Croissant', 'category': 'Food', 'price': 559, 'stock': 2, 'image': 'croissant.jpg'},
    {'id': 8, 'name': 'Caesar Salad', 'category': 'Food', 'price': 799, 'stock': 20, 'image': 'caesar-salad.jpg'},
    {'id': 9, 'name': 'Cinnamon Rolls', 'category': 'Food', 'price': 439, 'stock': 20, 'image': 'cinnamon-roll.jpg'},
]

# Tests can use a temporary file without changing the demonstration's orders.
DATA_FILE = Path(os.environ.get("CAFE_DATA_FILE", Path(__file__).with_name("cafe_data.json")))


def load_data():
    """Read saved orders and stock; return fresh menu data on the first run."""
    if not DATA_FILE.exists():
        return {"menu": [dict(item) for item in MENU], "orders": []}
    # Invalid storage raises an error instead of silently erasing sales history.
    with DATA_FILE.open(encoding="utf-8") as source:
        return json.load(source)


def save_data(state):
    """Save the supplied stock and orders together; return nothing."""
    temporary_file = DATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as destination:
        json.dump(state, destination, indent=2)
    # Replace only after the whole file is written, avoiding half-written JSON.
    temporary_file.replace(DATA_FILE)

````

### test_app.py

````python
"""Regression checks using Flask's test client and isolated temporary JSON files."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import data
from app import app
from logic import build_report


class CafeTests(unittest.TestCase):
    """Exercise ordering behavior without consuming the demonstration's inventory."""

    def setUp(self):
        """Create a fresh data path and client for each test; return nothing."""
        self.folder = tempfile.TemporaryDirectory()
        self.original_file = data.DATA_FILE
        data.DATA_FILE = Path(self.folder.name) / 'orders.json'
        app.config.update(TESTING=True, SECRET_KEY='test-only-key')
        self.client = app.test_client()

    def tearDown(self):
        """Restore the original storage path and delete test files; return nothing."""
        data.DATA_FILE = self.original_file
        self.folder.cleanup()

    def add(self, item='1', quantity='1'):
        """Submit an add-item request and return its final HTML response."""
        return self.client.post('/add-to-cart', data={'item_id': item, 'quantity': quantity}, follow_redirects=True)

    def checkout(self, **settings):
        """Submit checkout settings and return the redirect or error response."""
        return self.client.post('/checkout', data=settings)

    def test_empty_cart(self):
        """Empty checkout must not save an order."""
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Your cart is empty', response.data)
        self.assertEqual(data.load_data()['orders'], [])

    def test_bad_quantities(self):
        """Reject zero, negative, decimal, huge, nonnumeric, and missing additions."""
        for quantity in ['0', '-1', '1.5', '9' * 5000, 'coffee', '', '11']:
            with self.subTest(quantity=quantity[:20]):
                self.assertEqual(self.add(quantity=quantity).status_code, 200)
                with self.client.session_transaction() as browser:
                    self.assertEqual(browser.get('cart', {}), {})
        self.assertEqual(self.client.post('/add-to-cart', follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post('/update-cart', follow_redirects=True).status_code, 200)
        self.assertEqual(self.client.post('/remove-from-cart', follow_redirects=True).status_code, 200)
        self.assertIn(b'Choose an existing', self.add(item='bad').data)

    def test_sold_out_and_stock_limit(self):
        """Sold-out and over-stock additions are refused; accumulated limits hold."""
        self.assertIn(b'sold out', self.add('3').data)
        self.assertIn(b'Only 2', self.add('7', '3').data)
        self.add('1', '6')
        self.assertIn(b'limit is 10', self.add('1', '5').data)
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {'1': 6})

    def test_update_and_remove(self):
        """Updates reject invalid quantities and zero removes an existing item."""
        self.add()
        for quantity in ['-1', '1.1', 'abc', '11', '9' * 5000]:
            self.client.post('/update-cart', data={'item_id': '1', 'quantity': quantity})
            with self.client.session_transaction() as browser:
                self.assertEqual(browser['cart'], {'1': 1})
        self.client.post('/update-cart', data={'item_id': '1', 'quantity': '0'})
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {})
        self.add()
        self.client.post('/remove-from-cart', data={'item_id': 'bad'})
        self.client.post('/remove-from-cart', data={'item_id': '1'})
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {})

    def test_budget(self):
        """Reject overspending and malformed limits; an exact budget is allowed."""
        self.add()
        response = self.client.post('/checkout', data={'budget': '1'}, follow_redirects=True)
        self.assertIn(b'Budget exceeded', response.data)
        self.assertEqual(len(data.load_data()['orders']), 0)
        self.assertIn(b'Budget remaining: -$3.91', response.data)
        for budget in ['-1', '1.234', 'abc', '1e2']:
            self.assertEqual(self.checkout(budget=budget).status_code, 400)
        self.assertEqual(self.checkout(budget='4.91').status_code, 302)
        self.assertEqual(len(data.load_data()['orders']), 1)

    def test_delivery_discount_and_instructions(self):
        """Fees, discount rounding, instructions, and pickup totals persist correctly."""
        self.add()
        self.assertEqual(self.checkout(discount_code='bad').status_code, 400)
        self.assertEqual(self.checkout(fulfillment='unknown').status_code, 400)
        self.assertEqual(self.checkout(instructions='x' * 301).status_code, 400)
        self.assertEqual(data.load_data()['orders'], [])
        self.checkout(fulfillment='delivery', discount_code='cafe10', instructions='Extra hot')
        order = data.load_data()['orders'][0]
        self.assertEqual([order[k] for k in ['subtotal', 'discount', 'tax', 'delivery_fee', 'total']], [459, 46, 29, 399, 841])
        self.assertEqual(order['instructions'], 'Extra hot')
        self.add()
        self.checkout(fulfillment='pickup')
        self.assertEqual(data.load_data()['orders'][1]['total'], 491)
        self.assertEqual(data.load_data()['orders'][1]['delivery_fee'], 0)

    def test_preview_settings(self):
        """Saving settings changes the preview and keeps user entries visible."""
        self.add()
        response = self.client.post('/cart-settings', data={'fulfillment': 'delivery', 'budget': '20', 'instructions': 'Hi'}, follow_redirects=True)
        self.assertIn(b'action="/checkout"', response.data)
        self.assertIn(b'formaction="/cart-settings"', response.data)
        self.assertIn(b'$8.90', response.data)
        self.assertIn(b'$11.10', response.data)
        self.assertIn(b'Hi', response.data)
        self.assertEqual(data.load_data()['orders'], [])

    def test_checkout_rechecks_stock(self):
        """A second customer's purchase can exhaust inventory before checkout."""
        self.add('7', '2')
        other_customer = app.test_client()
        other_customer.post('/add-to-cart', data={'item_id': '7', 'quantity': '2'})
        other_customer.post('/checkout')
        response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'no longer has enough stock', response.data)
        self.assertEqual(len(data.load_data()['orders']), 1)
        self.assertEqual(data.load_data()['menu'][6]['stock'], 0)

    def test_receipt_refresh_and_restart(self):
        """Receipt GET is read-only and a fresh Python process sees saved stock/orders."""
        self.add()
        response = self.checkout()
        self.assertEqual(response.location, '/receipt/1')
        first = self.client.get(response.location)
        second = self.client.get(response.location)
        self.assertEqual(first.data, second.data)
        self.assertEqual(len(data.load_data()['orders']), 1)
        environment = dict(os.environ, CAFE_DATA_FILE=str(data.DATA_FILE))
        result = subprocess.check_output([os.sys.executable, '-c',
            'from data import load_data; s=load_data(); print(s["menu"][0]["stock"], len(s["orders"]))'], env=environment, text=True)
        self.assertEqual(result.strip(), '49 1')
        self.assertEqual(app.test_client().get('/receipt/1').status_code, 200)
        self.assertEqual(self.client.get('/receipt/999').status_code, 404)
        self.client.get('/receipt')
        self.assertEqual(len(data.load_data()['orders']), 1)

    def test_report_filters_and_sort(self):
        """Date/category filters and both sort choices affect the actual report data."""
        self.add('1', '1')
        self.add('6', '2')
        self.add('5', '4')
        self.checkout()
        state = data.load_data()
        for sort in ['revenue', 'quantity']:
            report, error = build_report(state['orders'], state['menu'], {'sort': sort})
            self.assertIsNone(error)
            expected = 'Black Coffee' if sort == 'quantity' else 'Blueberry Muffin'
            self.assertEqual(report['sales'][0]['name'], expected)
            self.assertEqual(report['best']['quantity'], 4)
            self.assertEqual(self.client.get('/report?sort=' + sort).status_code, 200)
        report, _ = build_report(state['orders'], state['menu'], {'category': 'Drinks'})
        self.assertEqual(len(report['sales']), 2)
        self.assertEqual(report['sales'][0]['name'], 'Black Coffee')
        self.assertEqual(report['revenue'], state['orders'][0]['total'])
        day = state['orders'][0]['timestamp'][:10]
        report, _ = build_report(state['orders'], state['menu'], {'start': day, 'end': day})
        self.assertEqual(len(report['orders']), 1)
        report, _ = build_report(state['orders'], state['menu'], {'end': '2000-01-01'})
        self.assertEqual(report['orders'], [])
        for query in ['start=bad', 'start=2026-02-30', 'start=2027-01-01&end=2020-01-01', 'category=Other', 'sort=bad']:
            self.assertEqual(self.client.get('/report?' + query).status_code, 400)

    def test_navigation_assets_and_help(self):
        """All main links/assets load and unknown questions receive a helpful answer."""
        for path in ['/', '/menu', '/cart', '/report', '/story', '/help', '/contact']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(b'href="#"', response.data)
                self.assertNotIn(b'src="script.js"', response.data)
        for asset in Path('static').rglob('*'):
            if asset.is_file() and not asset.name.startswith('.'):
                response = self.client.get('/' + asset.as_posix())
                self.assertEqual(response.status_code, 200)
                response.close()
        response = self.client.post('/help', data={'question': 'purple zebras?'})
        self.assertIn(b'Try asking about budget', response.data)
        response = self.client.post('/help', data={'question': 'What is my budget?'})
        self.assertIn(b'Set an optional budget', response.data)
        response = self.client.post('/help', data={'question': '<script>alert(1)</script>'})
        self.assertNotIn(b'<script>alert(1)</script>', response.data)

    def test_storage_failure_keeps_cart(self):
        """A failed save must not reduce stock or clear the customer's cart."""
        self.add()
        with patch('logic.save_data', side_effect=OSError('disk full')):
            response = self.client.post('/checkout', follow_redirects=True)
        self.assertIn(b'Could not save', response.data)
        self.assertEqual(data.load_data()['menu'][0]['stock'], 50)
        with self.client.session_transaction() as browser:
            self.assertEqual(browser['cart'], {'1': 1})


if __name__ == '__main__':
    unittest.main()

````

**What changed and why:** Routes delegate decisions to business logic. Prices use cents. Checkout checks stock and budget, saves orders with inventory, and redirects to a permanent receipt. Reports and keyword help use ordinary lists, dictionaries, loops, and functions. Tests cover the requested edge cases with isolated files.

## Batch 3 — Setup, disclosure, and presentation preparation

### README.md

````markdown
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

````

### requirements.txt

````text
# Flask is the only direct third-party library.
Flask==3.1.2

````

### .gitignore

````text
# Local environments, private settings, and demonstration order records.
.venv/
__pycache__/
*.pyc
cafe_data.json
cafe_data.tmp
.env
.DS_Store

````

### AI_Use.md

````markdown
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

````

### DEMO_NOTES.md

````markdown
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

````

### TEST_RESULTS.md

````markdown
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

````

**What changed and why:** Setup instructions describe Python and Flask accurately. Credits clearly identify missing information. The AI log discloses this session; demo notes provide a seven-minute walkthrough and fifteen practice questions. Test results state what was and was not verified.

