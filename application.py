import os
import re
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

admin_pwd="team_KV"
menus = [
    {
        'item_id':1,
        'item_name':'Rice',
        'description':'white rice',
        'price':30,
        'rating':4.0,
        'total':12
    },
    {
        'item_id':2,
        'item_name':'Roti',
        'description':'Roti',
        'price':15,
        'rating':4.0,
        'total':10
    }
]



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
            return redirect("/admin", code=307)
        else:
            return redirect("/")
    elif x:
        return redirect("/manager", code=307)
    elif y:
        return redirect("/delivery", code=307)
    else:
        return redirect("/cust", code=307)
    

@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")

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

@app.route("/admin", methods=["GET","POST"])
def admin():
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