from flask import Flask, render_template, request, session, redirect, url_for
from quizcardManager import QuizcardManager
from pathlib import Path

app = Flask(__name__)
app.secret_key = "basak"

# Use a relative path for the JSON file
file_path = Path(__file__).parent / "quizcards.json"
manager = QuizcardManager(file_path)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/general_biology_quiz/")
def quiz_home():
    return render_template("home.html")

@app.route("/general_biology_quiz/reset")
def reset():
    session.pop("current_question", None)
    session.pop("score", None)
    session.pop("answers", None)
    return redirect("/general_biology_quiz/")

@app.route("/general_biology_quiz/start_question", methods=["GET","POST"])
def start_question():
    if "current_question" not in session:
        session["current_question"] = 0 # Store the current question index
        session["score"] = 0 # Store user's score
        session["answers"] = []  # Store user's answers

    current_question = session["current_question"]
    if current_question >= len(manager.quizcards):
        # Quiz is complete, show the result
        score = session["score"]
        answers = session["answers"]
        # Reset session variables
        session.pop("current_question", "None")
        session.pop("score", "None")
        session.pop("answers", "None")

        return render_template("result.html", score=score, total=len(manager.quizcards), answers=answers)
        
    card = manager.quizcards[current_question]

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        is_correct = card.check_answer(user_answer)
        if is_correct:
            session["score"] += 1
        session["answers"].append({
            "term": card.term,
            "definition": card.definition,
            "user_answer": user_answer,
            "is_correct": is_correct
        })
        session["current_question"] += 1
        session.modified = True  # Save the session changes
        return redirect(url_for("start_question"))  # Pass to the next question

    return render_template("question.html", card=card, question_number=current_question + 1, total=len(manager.quizcards))

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5002, debug=True)
    except Exception as e:
        print("An error occurred while running the app:", e)