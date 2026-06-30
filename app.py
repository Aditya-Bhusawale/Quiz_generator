import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from werkzeug.utils import secure_filename

from src.rag import RAGPipeline
from src.quiz import QuizGenerator

app = Flask(__name__)
app.secret_key = "quiz_generator"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

rag = RAGPipeline()
quiz_generator = QuizGenerator()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    pdf = request.files.get("pdf")

    if not pdf or pdf.filename == "":
        return "Please select a PDF."

    filename = secure_filename(pdf.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    pdf.save(filepath)

    # Create Chroma collection
    collection_name = rag.process_pdf(filepath)

    # Store information in session
    session["collection"] = collection_name
    session["pdf_path"] = filepath

    return redirect(url_for("quiz_page"))


@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")


@app.route("/generate", methods=["POST"])
def generate():

    topic = request.form["topic"]
    difficulty = request.form["difficulty"]
    num_questions = int(request.form["num_questions"])

    collection_name = session.get("collection")

    if collection_name is None:
        return "Please upload a PDF first."

    retriever = rag.get_retriever(collection_name)

    quiz = quiz_generator.generate_quiz(
        retriever,
        topic,
        difficulty,
        num_questions
    )

    # Store quiz in session
    session["quiz"] = quiz.model_dump()

    return render_template(
        "quiz_display.html",
        questions=quiz.questions
    )

@app.route("/submit", methods=["POST"])
def submit():

    quiz = session["quiz"]

    score = 0
    results = []

    for i, question in enumerate(quiz["questions"]):

        user_answer = request.form.get(f"q{i}")

        correct_answer = question["answer"]

        if user_answer == correct_answer:
            score += 1

        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": user_answer == correct_answer
        })

    return render_template(
        "result.html",
        score=score,
        total=len(quiz["questions"]),
        results=results
    )

@app.route("/finish")
def cleanup():

    collection = session.get("collection")

    if collection:
        rag.load_collection(collection).delete_collection()

    pdf_path = session.get("pdf_path")

    if pdf_path and os.path.exists(pdf_path):
        os.remove(pdf_path)

    session.clear()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)