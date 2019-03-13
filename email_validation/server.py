from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re 
app = Flask(__name__)
app.secret_key = "secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_email():
    mysql = connectToMySQL("email_v")
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid Email!")
        return redirect("/")
    else:
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES ( %(email)s, NOW(), NOW());"
        data = {
            "email" : request.form["email"]
        }
        id = mysql.query_db(query, data)
        return redirect("/success")

@app.route("/success")
def success():
    mysql= connectToMySQL("email_v")
    query = ("SELECT * FROM emails")
    emails = mysql.query_db(query)
    return render_template("success.html", all_emails = emails)

if __name__ == "__main__":
    app.run(debug=True)