from flask import Flask, render_template, request, redirect, flash
#from data import 
#from logic import 

app = Flask(__name__)
app.secret_key = "fbla-demo"

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/menu")
def menu_page():
    query = request.args.get("q","")
    return render_template("menu.html", menu = search_menu(query))

@app.route("/cart")
def cart_page():
    # Cart page
    return render_template("cart.html")

@app.route("/receipt")
def receipt_page():
    # Put receipt details
    return render_template("receipt.html")

#Help and Contact Page
@app.route("/contact")
def contact_page():
    return render_template("contact.html")


