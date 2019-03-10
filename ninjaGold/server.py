from flask import Flask, request, session, render_template, redirect
import random
app=Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/')
def index():
    if 'money' not in session:
        session['money']= 0
    return render_template("index.html")

@app.route('/process_money', methods=["POST"])
def process_money():
    building = request.form['building']
    if building == 'farm':
        session['money'] += random.randint(10,20)
    elif building == 'cave':
        session['money'] += random.randint(5,10)
    elif building == 'house':
        session['money'] += random.randint(2,5)
    elif building == 'casino':
        session['money'] += random.randint(-50,50)
    return redirect('/')


if __name__==("__main__"):
    app.run(debug=True)