from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re 
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_user():
    pw_hash = bcrypt.generate_password_hash(request.form['pword'])
    print(pw_hash)
    mysql = connectToMySQL("login_registration")
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid Email!")
    if len(request.form["fname"]) < 1:
        is_valid = False
        flash("Please enter a first name.")
    if len(request.form["lname"]) < 1:
        is_valid = False
        flash("Please enter a last name.")
    if len(request.form["pword"]) < 1:
        is_valid = False
        flash("please enter a last name.")
    if request.form['pword'] != request.form['pwordconf']:
        flash("passwords do not match")
        return redirect("/")
    else:
        query = " INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pword_hash)s, NOW(), NOW());"
        data ={
            "first_name" : request.form["fname"],
            "last_name" : request.form["lname"],
            "email" : request.form["email"],
            "pword_hash" : pw_hash
        }
        id = mysql.query_db(query, data)
        session['userid'] = id
        session['logged in'] = True
        return redirect("/success/"+str(id))

@app.route("/login", methods=["POST"])
def login():
    mysql=connectToMySQL("login_registration")
    query="SELECT * FROM users WHERE email = %(email)s;"
    data = {"email" : request.form["email"]}
    result = mysql.query_db(query, data)
    print(result)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['pword']):
            session['userid'] = result[0]['id']
            session['logged_in'] = True
            return redirect("/success/"+str(result[0]['id']))
    flash("You could not be logged in")
    return redirect("/")

@app.route("/success/<id>")
def success(id):
    if 'userid' not in session:
        return redirect("/")
    else:
        mysql = connectToMySQL("login_registration")
        query = ("SELECT first_name FROM users WHERE id = %(id)s;")
        data = { "id" : id}
        names = mysql.query_db(query, data)
        print(names)
        return render_template("success.html", all_names = names)


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

