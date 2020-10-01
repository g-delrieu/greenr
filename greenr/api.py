from flask import Flask, redirect, url_for, render_template, request, jsonify
import main_calculation

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        url = request.form['url']
        score = main_calculation.calculate(url)
        rec = main_calculation.finding_better_recipe(score)
        return jsonify({"footprint per serving" : score[0],
                        "all_data" : score[1].to_json(orient="split"),
                        "title": score[3],
                        "url": score[4],
                        "recommended recipe" : rec["title"]})
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
