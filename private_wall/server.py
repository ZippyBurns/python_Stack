from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re 
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "zippys_key_is_a_secret"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/register", methods=["POST"])
def register_user():
    pw_hash = bcrypt.generate_password_hash(request.form['pword'])
    print(pw_hash)
    mysql = connectToMySQL("private_wall")
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid Email!")
    if len(request.form["full_name"]) < 1:
        is_valid = False
        flash("Please enter a first name.")
    if len(request.form["pword"]) < 1:
        is_valid = False
        flash("please enter a password.")
    if request.form['pword'] != request.form['pwordconf']:
        flash("passwords do not match")
        is_valid = False
    if is_valid == False:
        return redirect("/")
    else:
        mysql = connectToMySQL("private_wall")
        query = " INSERT INTO users (full_name, email, password, created_at, updated_at) VALUES (%(full_name)s, %(email)s, %(pword_hash)s, NOW(), NOW());"
        data ={
            "full_name" : request.form["full_name"],
            "email" : request.form["email"],
            "pword_hash" : pw_hash
        }
        id = mysql.query_db(query, data)
        session['userid'] = id
        session['logged in'] = True
        return redirect("/wall")

@app.route("/login", methods=["POST"])
def login():
    mysql=connectToMySQL("private_wall")
    query="SELECT * FROM users WHERE email = %(email)s;"
    data = {"email" : request.form["email"]}
    result = mysql.query_db(query, data)
    print(result)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['pword']):
            session['userid'] = result[0]['id']
            session['logged_in'] = True
            return redirect("/wall")
    flash("You could not be logged in")
    return redirect("/")

@app.route("/wall")
def success(): 
    if 'userid' not in session:
        return redirect("/")
    else:
        flash("You've logged in successfully!")
        mysql = connectToMySQL("private_wall")
        query = ("SELECT * FROM users WHERE id = %(session)s;")
        data={"session" : session['userid'] }
        current_user = mysql.query_db(query, data)
        print("***current_user***",current_user)
        
        mysql = connectToMySQL("private_wall")
        user_query = ("SELECT * FROM users WHERE id != %(session)s")
        all_users = mysql.query_db(user_query, data)
        
        mysql = connectToMySQL("private_wall")
        message_query = "SELECT * FROM messages INNER JOIN users ON messages.sender_id = users.id WHERE receiver_id = %(session)s"
        messages = mysql.query_db(message_query, data)
        return render_template("wall.html", current_user = current_user, all_users = all_users, all_messages = messages)

    

@app.route("/send_message", methods=["POST"])
def send_message():
    print(request.form)
    mysql = connectToMySQL("private_wall")
    query = "INSERT INTO messages (content, created_at, updated_at, sender_id, receiver_id) VALUES (%(content)s, NOW(), NOW(), %(session)s, %(recid)s);"
    data = { "session" : session['userid'],
        "content" : request.form['message'],
        "recid" : int(request.form['receiver_id'])
    }
    messages = mysql.query_db(query, data)
    flash("Your message has been sent!")
    print("**** MESSAGES ****", messages)
    return redirect ("/wall")

@app.route("/delete/<id>")
def delete_message(id):
    mysql = connectToMySQL("private_wall")
    query ="DELETE FROM messages WHERE id = %(id)s "
    data ={
        "id" : id}
    mysql.query_db(query,data)
    flash("Message deleted")
    return redirect("/wall")
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)