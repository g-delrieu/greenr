from flask import Flask, redirect, url_for, render_template, request
import main_calculation

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        url = request.form['url']
        score = main_calculation.calculate(url)
        return score
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
