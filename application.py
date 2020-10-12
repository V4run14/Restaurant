import os
import re
from flask import Flask, render_template, request, redirect, url_for
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
        managers = db.execute("SELECT manager_id, pwd FROM manager WHERE email= :email",
            {"email": email}).fetchone()
        if managers is None:
            return redirect("/")
        elif pwd == managers.pwd:
            return redirect(url_for('manager_prof', manager_id=managers.manager_id), code=307)    
        else:
            return redirect("/")
    elif y:
        dboys = db.execute("SELECT dboy_id, pwd FROM delivery WHERE email= :email",
            {"email": email}).fetchone()
        if dboys is None:
            return redirect("/")
        elif pwd == dboys.pwd:
            return redirect(url_for('dboy_prof', dboy_id=dboys.dboy_id), code=307)    
        else:
            return redirect("/")
    else:
        cust = db.execute("SELECT cust_id, pwd FROM customer WHERE email= :email",
            {"email": email}).fetchone()
        if cust is None:
            return redirect("/")
        elif pwd == cust.pwd:
            return redirect(url_for('cust_prof', cust_id=cust.cust_id), code=307)    
        else:
            return redirect("/")
    

@app.route("/register", methods=["GET","POST"])
def register():
    areas = db.execute("SELECT branch_name, area_code FROM branches B JOIN area_codes A ON (B.branch_id=A.branch_id)").fetchall()
    return render_template("register.html", areas=areas)

@app.route("/register1", methods=["POST"])
def register1():
    fname = request.form.get("fname"); lname = request.form.get("lname"); mob = request.form.get("mob")
    address = request.form.get("address"); ar_cod = request.form.get("area_code"); age = request.form.get("age")
    email = request.form.get("email"); pwd = request.form.get("pwd"); cnf = request.form.get("cnf")
    if pwd==cnf:
        db.execute("INSERT INTO customer (fname, lname, cust_ph, email, pwd, address, area_code, age) VALUES ( :fname, :lname, :cust_ph, :email, :pwd, :address, :area_code, :age)",
            {"fname": fname, "lname": lname, "cust_ph": mob, "email": email, "pwd": pwd, "address": address, "area_code": ar_cod, "age": age})
        db.commit()
        return redirect("/")
    else:
        return redirect("/register", code=307)

@app.route("/admin/menu", methods=["GET","POST"])
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
        return render_template("admin_menu_additem.html")


@app.route("/admin/branch", methods=["GET","POST"])
def admin_branch():
    if request.form.get("branch_name"):
        branch_name = request.form.get("branch_name"); address = request.form.get("address")
        ac1 = request.form.get("area_code1"); ac2 = request.form.get("area_code2"); ac3 = request.form.get("area_code3")
        manager_name = request.form.get("manager_name"); manager_ph = request.form.get("manager_ph"); age = request.form.get("age")
        email = request.form.get("email"); pwd = request.form.get("pwd")
        db.execute("INSERT INTO branches (branch_name, address) VALUES (:branch_name, :address)",
            {"branch_name": branch_name, "address": address})
        db.execute("INSERT INTO manager (manager_name, manager_ph, email, pwd, age) VALUES (:manager_name, :manager_ph, :email, :pwd, :age)",
            {"manager_name": manager_name, "manager_ph": manager_ph, "email": email, "pwd": pwd, "age": age})
        db.commit()
        br = db.execute("SELECT branch_id FROM branches WHERE branch_name= :branch_name",
            {"branch_name": branch_name}).fetchone()
        b = br.branch_id
        db.execute("INSERT INTO area_codes (branch_id, area_code) VALUES (:branch_id, :area_code)",
            {"branch_id": b, "area_code": ac1})
        db.execute("INSERT INTO area_codes (branch_id, area_code) VALUES (:branch_id, :area_code)",
            {"branch_id": b, "area_code": ac2})
        db.execute("INSERT INTO area_codes (branch_id, area_code) VALUES (:branch_id, :area_code)",
            {"branch_id": b, "area_code": ac3})
        db.commit()
    branches = db.execute("SELECT A.branch_id, branch_name, address, manager_name, manager_ph FROM branches A JOIN manager B ON (A.branch_id=B.branch_id)").fetchall()
    area_codes = db.execute("SELECT * FROM area_codes").fetchall()
    return render_template("admin_branch.html",branches=branches, area_codes=area_codes)

@app.route("/admin/branch/edit", methods=["GET","POST"])
def admin_branch_edit():
    if request.method == "POST":
        branch_id = request.form.get("branch_id")
        db.execute("DELETE FROM branches WHERE branch_id = :branch_id",
            {"branch_id": branch_id})
        db.execute("DELETE FROM manager WHERE branch_id = :branch_id",
            {"branch_id": branch_id})
        db.execute("DELETE FROM delivery WHERE manager_id = :branch_id",
            {"branch_id": branch_id})
        db.execute("DELETE FROM area_codes WHERE branch_id = :branch_id",
            {"branch_id": branch_id})
        db.commit()
        return redirect("/admin/branch", code=307)
    else: 
        return render_template("admin_branch_addbranch.html")

@app.route("/admin/order", methods=["GET","POST"])
def admin_order():
    orders = db.execute("SELECT * FROM orders").fetchall()
    items = db.execute("SELECT order_id, B.item_id, item_name, quantity FROM menu A JOIN order_items B ON(A.item_id=B.item_id)").fetchall()
    return render_template("admin_order.html", orders=orders, items=items)

@app.route("/manager/<int:manager_id>/profile", methods=["GET","POST"])
def manager_prof(manager_id):
    if request.form.get("age"):
        manager_name = request.form.get("manager_name"); ph = request.form.get("manager_ph")
        pwd = request.form.get("pwd"); age = request.form.get("age")
        db.execute("UPDATE manager SET manager_name= :manager_name, manager_ph= :manager_ph, pwd= :pwd, age= :age WHERE manager_id= :manager_id",
            {"manager_name": manager_name, "manager_ph": ph, "pwd": pwd, "age": age, "manager_id": manager_id})
        db.commit()
    profile = db.execute("SELECT * FROM manager WHERE manager_id= :manager_id",
        {"manager_id":manager_id}).fetchone()
    branch = db.execute("SELECT branch_name FROM branches WHERE branch_id= :manager_id",
        {"manager_id":manager_id}).fetchone()
    return render_template("manager_profile.html", profile=profile, branch=branch)

@app.route("/manager/<int:manager_id>/profile/edit", methods=["GET","POST"])
def manager_prof_edit(manager_id):
    profile = db.execute("SELECT * FROM manager WHERE manager_id= :manager_id",
        {"manager_id":manager_id}).fetchone()
    return render_template("manager_profile_edit.html", profile=profile)

@app.route("/manager/<int:manager_id>/deliv", methods=["GET","POST"])
def manager_deliv(manager_id):
    if request.form.get("dboy_name"):
        dboy_name = request.form.get("dboy_name"); IDD = manager_id
        area_code = request.form.get("area_code"); dboy_ph = request.form.get("dboy_ph"); age = request.form.get("age")
        email = request.form.get("email"); pwd = request.form.get("pwd")
        db.execute("INSERT INTO delivery (dboy_name, dboy_ph, email, pwd, age, manager_id, area_code) VALUES (:dboy_name, :dboy_ph, :email, :pwd, :age, :manager_id, :area_code)",
            {"dboy_name": dboy_name, "dboy_ph": dboy_ph, "email": email, "pwd": pwd, "age": age, "manager_id":IDD, "area_code": area_code})
        db.commit()
    deliv = db.execute("SELECT * FROM delivery WHERE manager_id= :manager_id",
        {"manager_id": manager_id}).fetchall()
    ID = db.execute("SELECT manager_id FROM delivery WHERE manager_id= :manager_id",
        {"manager_id": manager_id}).fetchone()
    return render_template("manager_deliv.html", deliv=deliv, ID=ID)

@app.route("/manager/<int:manager_id>/deliv/edit", methods=["GET","POST"])
def manager_deliv_edit(manager_id):
    ID = manager_id
    if request.method == "POST":
        dboy_id = request.form.get("dboy_id")
        db.execute("DELETE FROM delivery WHERE dboy_id = :dboy_id",
            {"dboy_id": dboy_id})
        db.commit()
        return redirect(url_for('manager_deliv', manager_id=ID), code=307)
    else:
        areas = db.execute("SELECT area_code FROM branches B JOIN area_codes A ON (B.branch_id=A.branch_id) WHERE A.branch_id= :ID",
            {"ID": ID}).fetchall()
        return render_template("manager_deliv_edit.html",ID=ID, areas=areas)

@app.route("/manager/<int:manager_id>/order", methods=["GET","POST"])
def manager_order(manager_id):
    orders = db.execute("SELECT * FROM orders WHERE branch_id= :manager_id",
        {"manager_id":manager_id}).fetchall()
    ID = db.execute("SELECT branch_id FROM orders WHERE branch_id= :manager_id",
        {"manager_id":manager_id}).fetchone()
    items = db.execute("SELECT order_id, B.item_id, item_name, quantity FROM menu A JOIN order_items B ON(A.item_id=B.item_id)").fetchall()
    return render_template("manager_order.html", orders=orders, items=items, ID=ID)


@app.route("/dboy/<int:dboy_id>/profile", methods=["GET","POST"])
def dboy_prof(dboy_id):
    if request.form.get("age"):
        dboy_name = request.form.get("dboy_name"); dboy_ph = request.form.get("dboy_ph")
        pwd = request.form.get("pwd"); age = request.form.get("age")
        db.execute("UPDATE delivery SET dboy_name= :dboy_name, dboy_ph= :dboy_ph, pwd= :pwd, age= :age WHERE dboy_id= :dboy_id",
            {"dboy_name": dboy_name, "dboy_ph": dboy_ph, "pwd": pwd, "age": age, "dboy_id": dboy_id})
        db.commit()
    profile = db.execute("SELECT * FROM delivery WHERE dboy_id= :dboy_id",
        {"dboy_id":dboy_id}).fetchone()
    manager = db.execute("SELECT manager_id, manager_name, manager_ph FROM manager WHERE manager_id= :manager_id",
        {"manager_id":profile.manager_id}).fetchone()
    branch = db.execute("SELECT branch_name FROM branches WHERE branch_id= :manager_id",
        {"manager_id":profile.manager_id}).fetchone()
    return render_template("dboy_profile.html", profile=profile, manager=manager, branch=branch)

# in profile tab use {{url_for('dboy_prof', dboy_id=profile.dboy_id)}} and {{url_for('dboy_order', dboy_id=profile.dboy_id)}}

@app.route("/dboy/<int:dboy_id>/profile/edit", methods=["GET","POST"])
def dboy_prof_edit(dboy_id):
    profile = db.execute("SELECT * FROM delivery WHERE dboy_id= :dboy_id",
        {"dboy_id":dboy_id}).fetchone()
    return render_template("dboy_profile_edit.html", profile=profile)

@app.route("/dboy/<int:dboy_id>/order", methods=["GET","POST"])
def dboy_order(dboy_id):
    orders = db.execute("SELECT * FROM orders WHERE dboy_id= :dboy_id",
        {"dboy_id":dboy_id}).fetchall()
    ID = db.execute("SELECT dboy_id FROM orders WHERE dboy_id= :dboy_id",
        {"dboy_id":dboy_id}).fetchone()
    items = db.execute("SELECT order_id, B.item_id, item_name, quantity FROM menu A JOIN order_items B ON(A.item_id=B.item_id)").fetchall()
    return render_template("dboy_order.html", orders=orders, items=items, ID=ID)



@app.route("/cust/<int:cust_id>/profile", methods=["GET","POST"])
def cust_prof(cust_id):
    if request.form.get("age"):
        fname = request.form.get("fname"); lname = request.form.get("lname"); cust_ph = request.form.get("cust_ph")
        address = request.form.get("address"); area_code = request.form.get("area_code"); pwd = request.form.get("pwd"); age = request.form.get("age")
        db.execute("UPDATE customer SET fname= :fname, lname= :lname, cust_ph= :cust_ph, address= :address, area_code= :area_code, pwd= :pwd, age= :age WHERE cust_id= :cust_id" ,
            {"fname": fname, "lname": lname, "cust_ph": cust_ph, "address": address, "area_code": area_code, "pwd": pwd, "age": age, "cust_id": cust_id})
        db.commit()
    profile = db.execute("SELECT * FROM customer WHERE cust_id= :cust_id",
        {"cust_id":cust_id}).fetchone()
    return render_template("cust_profile.html", profile=profile)

@app.route("/cust/<int:cust_id>/profile/edit", methods=["GET","POST"])
def cust_prof_edit(cust_id):
    profile = db.execute("SELECT * FROM customer WHERE cust_id= :cust_id",
        {"cust_id":cust_id}).fetchone()
    return render_template("cust_profile_edit.html", profile=profile)

@app.route("/cust/<int:cust_id>/place_order", methods=["GET","POST"])
def cust_place_order(cust_id):
    ID = cust_id
    menus = db.execute("SELECT * FROM menu").fetchall()
    areas = db.execute("SELECT branch_name, area_code FROM branches B JOIN area_codes A ON (B.branch_id=A.branch_id)").fetchall()
    profile = db.execute("SELECT * FROM customer WHERE cust_id= :cust_id",
        {"cust_id":cust_id}).fetchone()
    # display menu items with buttons to inc and dec qty and input fields for address and drop down of area code with default values
    # for quantity input, let name be item_id variable and value be the quantity
    # route place order button to order history
    return render_template("cust_place_order.html",menus=menus, ID=ID, areas=areas, profile=profile)


@app.route("/cust/<int:cust_id>/order", methods=["GET","POST"])
def cust_order(cust_id):
    ID = cust_id
    orders = db.execute("SELECT * FROM orders WHERE cust_id= :cust_id",
        {"cust_id":cust_id}).fetchall()
    #ID = db.execute("SELECT cust_id FROM orders WHERE cust_id= :cust_id",
        #{"cust_id":cust_id}).fetchone()
    items = db.execute("SELECT order_id, B.item_id, item_name, quantity FROM menu A JOIN order_items B ON(A.item_id=B.item_id)").fetchall()
    return render_template("cust_order.html", orders=orders, items=items, ID=ID)