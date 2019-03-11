from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route('/')
def index():
    mysql = connectToMySQL("mydb")
    pets = mysql.query_db("SELECT * FROM pets;")
    print(pets)
    return render_template("index.html", all_pets = pets)

@app.route('/create_pet', methods=["POST"])
def create_pet():
    print(request.form)
    mysql= connectToMySQL("mydb")
    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(pname)s, %(ptype)s, NOW(), NOW());"
    data = {
        "pname": request.form["pname"],
        "ptype": request.form["ptype"]
    }
    new_pet = mysql.query_db(query,data)
    print(new_pet)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)