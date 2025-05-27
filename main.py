from flask import Flask, render_template, request, session, redirect, url_for
from quizcardManager import QuizcardManager
from pathlib import Path

app = Flask(__name__)
app.secret_key = "basak"

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
        session["current_question"] = 0 #current question number
        session["score"] = 0 #user's score
        session["answers"] = []  #user's answers

    current_question = session["current_question"]
    if current_question >= len(manager.quizcards):
        score = session["score"] #quiz is completed, show the result
        answers = session["answers"]
        
        #reset session variables
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
            "is_correct": is_correct})
        session["current_question"] += 1
        session.modified = True  #save the session changes
        return redirect(url_for("start_question"))  #pass to the next question

    return render_template("question.html", card=card, question_number=current_question + 1, total=len(manager.quizcards))

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5002, debug=True)
    except Exception as e:
        print("An error occurred while running the app:", e)