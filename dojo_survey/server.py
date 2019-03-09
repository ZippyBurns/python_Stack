from flask import Flask, render_template,request, redirect
app = Flask(__name__)
@app.route('/')
def info():
    return render_template("index.html")

@app.route('/result', methods=['POST'])
def results():
    print("Got Post info!")
    print(request.form)
    name_from_form = request.form['name']
    return render_template("result.html", name_on_template=name_from_form)

if __name__==("__main__"):
    app.run(debug=True)