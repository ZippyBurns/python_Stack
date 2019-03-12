from flask import Flask, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "secret"
@app.route("/")
def index():
    return redirect("/all_users")

@app.route("/create_user")
def create_user_page():
    return render_template ("create_user.html")

@app.route("/create_user", methods=["POST"])
def add_user_to_db():
    print (request.form)
    mysql = connectToMySQL("user")
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES ( %(first)s, %(last)s, %(email)s, NOW(), NOW());"
    data = {
        "first": request.form["fname"],
        "last": request.form["lname"],
        "email" : request.form["email"]
    }
    id = mysql.query_db(query, data)
    return redirect("/users/"+str(id))

@app.route("/users/<id>")
def display_user(id):
    mysql = connectToMySQL("user")
    query = ("SELECT * FROM users WHERE id = %(uid)s;")
    data = {
        "uid" : id
    }
    users = mysql.query_db(query,data)
    print(users) 
    return render_template("users.html", all_users = users)

@app.route("/users/<id>/edit")
def go_to_edit(id):
    return render_template("edit.html", id=id)

@app.route("/users/<id>/edit", methods=["POST"])
def edit_user(id):
    mysql = connectToMySQL("user")
    query = "UPDATE users SET first_name = %(first)s, last_name = %(last)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
    data = {
        "first": request.form["fname"],
        "last": request.form["lname"],
        "email": request.form["email"],
        "id" : id
    }
    print("Working!!")
    myid = mysql.query_db(query, data)
    return redirect("/users/"+str(id))


@app.route("/users/<id>/delete")
def delete_user(id):
    print("i'm here!")
    mysql = connectToMySQL("user")
    query = "DELETE FROM users WHERE id = %(id)s"
    data = {
        "id" : id
    }
    myid = mysql.query_db(query,data)
    return redirect("/")

@app.route("/all_users")
def all_users():
    mysql = connectToMySQL("user")
    users = mysql.query_db ("SELECT * FROM users")
    print(users) 
    return render_template("all_users.html", all_users = users)

if __name__ == "__main__":
    app.run(debug=True)



