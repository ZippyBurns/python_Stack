from flask import Flask, render_template, request, redirect, session
from multiprocessing import Value
app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    if 'count' in session:
        print('key exists!')
        session['count'] += 1
    else:
        session['count'] = 1
        print("key 'key_name' does NOT exist")
    return render_template('index.html', session = session)
        

@app.route('/counter')
def add2Visits():
    session ['count'] += 1
    return redirect('/')
    


if __name__=="__main__":
    app.run (debug=True)




