from flask import Flask, render_template, request, redirect, url_for, flash
from forms import AddressForm, LoginForm, SignupForm, CheckoutForm, Feedbackform
from perfumes import perfumes  # Importing the perfumes dictionary
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # Added for password hashing
import os  # For secure secret key

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24).hex()  # Secure random key; or use an env var like os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stor.db'
db = SQLAlchemy(app)

class Store(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Now hashed

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Orderplace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(100), nullable=False)
    perfume_id = db.Column(db.Integer, nullable=True)   # Added to link to specific perfume
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html", title="Welcome to Noxy perfumes")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Store.query.filter_by(email=email).first()
        
        if user and user.check_password(password):  # Now checks hashed password
            return redirect(url_for("showproduct"))
        else:
            flash("Invalid login details")
    
    return render_template("login.html", title="LOGIN PAGE", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = Store(name=form.username.data, email=form.email.data, phone_number=form.phone_number.data)
        new_user.set_password(form.password.data)  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        flash("Signup success")
        return redirect(url_for("login"))
    return render_template("signup.html", title="SIGNUP PAGE", form=form)

@app.route("/shopnow")
def shopnow():
    # If you want to show perfumes without login, uncomment below:
    # return render_template("shopnow.html", perfumes=perfumes)
    return redirect(url_for("login"))

@app.route("/deliveryinfo", methods=["GET", "POST"])
def deliveryinfo(): 
    form = AddressForm()
    perfume_id = request.args.get("perfume_id")
    if perfume_id:
        perfume_id = int(perfume_id)  # Convert to int to match db.Column(db.Integer)
    if form.validate_on_submit():
        delivery = Orderplace(name=form.name.data, email=form.email.data, phone_number=form.phone_number.data, address=form.address.data, pincode=form.pincode.data, perfume_id=perfume_id)  # Added perfume_id
        db.session.add(delivery)
        db.session.commit()
        return redirect(url_for("payments", perfume_id=perfume_id))
    return render_template("deliveryinfo.html", title="Delivery Info", form=form, perfume_id=perfume_id)

@app.route("/about")
def knowmore():
    return render_template("about.html", title="ABOUT PAGE")

@app.route("/newarrivals")
def newarrivals():
    # Filter for new perfumes if needed
    new_perfumes = {k: v for k, v in perfumes.items() if v.get('new')}
    return render_template("newarrivals.html", title="NEW ARRIVALS", perfumes=new_perfumes)

@app.route("/offersection")
def offersection():
    # Filter for offer perfumes if needed
    offer_perfumes = {k: v for k, v in perfumes.items() if v.get('offer')}
    return render_template("offersection.html", title="GRAB YOUR PERFUME", perfumes=offer_perfumes)

@app.route("/help")
def help():
    return render_template("help.html", title="HELP")

@app.route("/payments", methods=["GET", "POST"])
def payments():
    form = CheckoutForm()
    perfume_id = request.args.get("perfume_id")
    selected_perfume = perfumes.get(perfume_id)


    if form.validate_on_submit():
        return redirect(url_for("ordersuccess"))

    return render_template("payments.html", form=form, perfumes=selected_perfume)  # Kept as 'perfumes' for template consistency

@app.route("/perfumeuse")
def perfumecaredetails():
    return render_template("perfumeuse.html")

@app.route("/ordernow")
def ordernow():
    # If this is a general button, redirect to showproduct or pass a default perfume_id
    return redirect(url_for("showproduct"))

@app.route("/ordersuccess")
def ordersuccess():
    return render_template("ordersuccess.html", title="SUCCESS")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = Feedbackform()
    if form.validate_on_submit():
        return redirect(url_for("feedback"))
    return render_template("contact.html", title="CONTACT us", form=form)

@app.route("/showproduct")
def showproduct():
    return render_template("showproduct.html", title="AVAILABLE PRODUCTS", perfumes=perfumes)

@app.route("/perfume/<perfume_id>")
def perfume_detail(perfume_id):
    perfume = perfumes.get(perfume_id)
    if perfume:
        return render_template("perfume_detail.html", title="DETAILS", perfumes=perfume, perfume_key=perfume_id)
    else:
        flash("Perfume not found.")
        return redirect(url_for("showproduct"))

@app.route("/faqs")
def faqs():
    return render_template("faqs.html", title="FAQS")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html", title="FEEDBACK")

@app.route("/wishlist")
def wishlist():
    # For user-specific wishlists, you'd need session/user auth and DB storage
    return render_template("wishlist.html", title="WISHLIST", perfumes=perfumes)

if __name__ == "__main__":
    app.run(debug=True)
