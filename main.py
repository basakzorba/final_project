from flask import Flask, render_template, request, session, redirect, url_for
from flashcardManager import FlashcardManager
from pathlib import Path

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management
file_path = Path("/Users/basakisilzorba/Desktop/REDI/Python_2025/Lessons/python_projects/Redi_python_s25/Final_Project/flashcards.json")
manager = FlashcardManager(file_path)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/reset")
def reset():
    session.pop("current_question", None)
    session.pop("score", None)
    session.pop("answers", None)
    return redirect("/")

@app.route("/start_quiz", methods=["GET", "POST"])
def start_quiz():
    if "current_question" not in session:
        session["current_question"] = 0
        session["score"] = 0
        session["answers"] = []  # Store user's answers and correctness

    current_question = session["current_question"]
    if current_question >= len(manager.flashcards):
        # Quiz is complete, show the result
        score = session["score"]
        answers = session["answers"]
        session.pop("current_question", None)
        session.pop("score", None)
        session.pop("answers", None)
        return render_template("result.html", score=score, total=len(manager.flashcards), answers=answers)

    card = manager.flashcards[current_question]

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
        session.modified = True  # Ensure session changes are saved
        return redirect(url_for("start_quiz"))  # Redirect to the next question

    return render_template("question.html", card=card, question_number=current_question + 1, total=len(manager.flashcards))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)