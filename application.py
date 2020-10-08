import os
import re
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    
    #return redirect("/register", code=307)
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    #return "Login page"
    email = request.form.get("email")
    x = re.search("@manager.com" , email)
    y = re.search("@delivery.com" , email)
    if email == "admin@admin.com":
        return redirect("/admin", code=307)
    elif x:
        return redirect("/manager", code=307)
    elif y:
        return redirect("/delivery", code=307)
    else:
        return redirect("/cust", code=307)
    

@app.route("/register", methods=["POST"])
def register():
    return "you have been redirected"

@app.route("/admin", methods=["POST"])
def admin():
    return "This is the admin view"

@app.route("/manager", methods=["POST"])
def manager():
    return "This is the manager view"

@app.route("/cust", methods=["POST"])
def cust():
    return "This is the customer view"

@app.route("/delivery", methods=["POST"])
def delivery():
    return "This is the delivery boy view"