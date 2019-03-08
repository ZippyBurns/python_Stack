from flask import Flask, render_template
app = Flask(__name__)
@app.route('/checkers/<x>/<y>')
def checkers(x,y):
    return render_template("checker.html", xtimes=int(x), ytimes=int(y))

if __name__=="__main__":
    app.run(debug=True)