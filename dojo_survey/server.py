from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/survey", methods=["POST"])
def survey():
    mysql = connectToMySQL("survey")
    is_valid = True
    if len(request.form["fname"]) < 1:
        is_valid = False
        flash("Please enter a first name.")
    if len(request.form["lname"]) < 1:
        is_valid = False
        flash("Please enter a last name.")
    if len(request.form["comment"]) < 1:
        is_valid = False
        flash("Please enter a comment.")
    if not is_valid:
        return redirect("/")
    else:
        flash("Success!!")  
    query = "INSERT INTO students (first_name, last_name, location, fav_lang, comment, created_at, updated_at) VALUES (%(first)s, %(last)s, %(location)s, %(fav)s, %(comment)s, NOW(), NOW());"
    data = {
        "first": request.form["fname"],
        "last": request.form["lname"],
        "location": request.form["loc"],
        "fav": request.form["fav"],
        "comment": request.form["comment"]
    }
    myid = mysql.query_db(query, data)
    return redirect("/results")

@app.route("/results")
def show_results():
    mysql = connectToMySQL("survey")
    students = mysql.query_db("SELECT * FROM students")
    print(students)
    return render_template ("results.html", all_students = students)

if __name__ == "__main__":
    app.run(debug=True)