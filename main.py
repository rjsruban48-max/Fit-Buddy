from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/plan", methods=["GET", "POST"])
def plan():

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        goal = request.form.get("goal")
        fitness_level = request.form.get("fitness_level")

        workout = [
            "Warm-up - 5 minutes",
            "Bodyweight squats - 3 sets",
            "Push-ups - 3 sets",
            "Light cardio - 15 minutes",
            "Cool-down - 5 minutes"
        ]

        tips = [
            "Stay hydrated.",
            "Get enough sleep.",
            "Take rest when needed.",
            "Increase activity gradually."
        ]

        return render_template(
            "plan.html",
            name=name,
            age=age,
            goal=goal,
            fitness_level=fitness_level,
            workout=workout,
            tips=tips,
            generated=True
        )

    return render_template("plan.html", generated=False)


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)