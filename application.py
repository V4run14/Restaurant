import os

from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    
    #return redirect("/register", code=307)
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    #return "Login page"
    return redirect("/register", code=307)
    # Get form information.
    #name = request.form.get("name")

@app.route("/register", methods=["POST"])
def register():
    return "you have been redirected"
    #return render_template("index.html")
    # Get form information.
    #name = request.form.get("name")