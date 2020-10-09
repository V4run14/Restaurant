import os
import re
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

admin_pwd="team_KV"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    #return "Login page"
    email = request.form.get("email")
    pwd = request.form.get("pwd")
    x = re.search("@manager.com" , email)
    y = re.search("@delivery.com" , email)
    if email == "admin@admin.com":
        if pwd == admin_pwd:
            return redirect("/admin/menu", code=307)
        else:
            return redirect("/")
    elif x:
        return redirect("/manager", code=307)
    elif y:
        return redirect("/delivery", code=307)
    else:
        return redirect("/cust", code=307)
    

@app.route("/register", methods=["GET","POST"])
def register():
    areas = db.execute("SELECT branch_name, area_code FROM branches B JOIN area_codes A ON (B.branch_id=A.branch_id) ").fetchall()
    return render_template("register.html", areas=areas)

@app.route("/register1", methods=["POST"])
def register1():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    mob = request.form.get("mob")
    address = request.form.get("address")
    ar_cod = request.form.get("area_code")
    age = request.form.get("age")
    email = request.form.get("email") 
    pwd = request.form.get("pwd")
    cnf = request.form.get("cnf")
    if pwd==cnf:
        #commit data into database
        return redirect("/")
    else:
        return redirect("/register", code=307)

@app.route("/admin/menu", methods=["POST"])
def admin_menu():
    if request.form.get("item_name"):
        item_name = request.form.get("item_name")
        description = request.form.get("description")
        price = request.form.get("price")
        db.execute("INSERT INTO menu (item_name, description, price, rating, votes) VALUES (:item_name, :description, :price, 0.0, 0)",
            {"item_name": item_name, "description": description, "price": price})
        db.commit()
    menus = db.execute("SELECT * FROM menu").fetchall()
    return render_template("admin_menu.html",menus=menus)

@app.route("/admin/menu/edit", methods=["GET","POST"])
def admin_menu_edit():
    if request.method == "POST":
        item_id = request.form.get("item_id")
        db.execute("DELETE FROM menu WHERE item_id = :item_id",
            {"item_id": item_id})
        db.commit()
        return redirect("/admin/menu", code=307)
    else: 
        flag=1
        return render_template("admin_menu_additem.html")


@app.route("/admin/branch", methods=["GET","POST"])
def admin_branch():
    return render_template("admin_branch.html")

@app.route("/admin/branch/edit", methods=["GET","POST"])
def admin_branch_edit():
    if request.method == "POST":
        # take item id and process the query for deletion 
        return render_template("admin_branch.html")
    else: 
        return render_template("admin_branch_addbranch.html")


@app.route("/admin/order", methods=["GET","POST"])
def admin_order():
    return render_template("admin.html")

@app.route("/manager", methods=["POST"])
def manager():
    return "This is the manager view"

@app.route("/cust", methods=["POST"])
def cust():
    return "This is the customer view"

@app.route("/delivery", methods=["POST"])
def delivery():
    return "This is the delivery boy view"