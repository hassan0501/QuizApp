
from flask import Flask, render_template, request, redirect, url_for, session
from dsa_structures import Array, Stack, Queue, LinkedList
import json
import os

app = Flask(__name__)
app.secret_key = "dsa-quiz-secret-key"


subjects = {
    "dsa": {
        "name": "DSA",
        "questions": [
            {
                "question": "Which data structure follows LIFO?",
                "options": ["Queue", "Stack", "Array", "Tree"],
                "answer": "Stack"
            },
            {
                "question": "Which data structure follows FIFO?",
                "options": ["Stack", "Queue", "Tree", "Graph"],
                "answer": "Queue"
            }
        ]
    },

    "bel": {
        "name": "BEL",
        "questions": [
            {
                "question": "Which component allows current to flow mainly in one direction?",
                "options": ["Resistor", "Diode", "Capacitor", "Switch"],
                "answer": "Diode"
            },
            {
                "question": "Which component stores electrical charge?",
                "options": ["Capacitor", "Diode", "Fuse", "Transistor"],
                "answer": "Capacitor"
            },
            {
                "question": "What is the unit of resistance?",
                "options": ["Volt", "Ampere", "Ohm", "Watt"],
                "answer": "Ohm"
            },
            {
                "question": "Which device can amplify electronic signals?",
                "options": ["Resistor", "Transistor", "Fuse", "Switch"],
                "answer": "Transistor"
            },
            {
                "question": "What is the unit of capacitance?",
                "options": ["Henry", "Farad", "Ohm", "Tesla"],
                "answer": "Farad"
            },
            {
                "question": "Which component protects a circuit against excessive current?",
                "options": ["Capacitor", "LED", "Fuse", "Resistor"],
                "answer": "Fuse"
            },
            {
                "question": "What does LED stand for?",
                "options": [
                    "Light Emitting Diode",
                    "Low Energy Device",
                    "Light Electrical Display",
                    "Linear Emitting Device"
                ],
                "answer": "Light Emitting Diode"
            },
            {
                "question": "Which material is commonly used in semiconductor devices?",
                "options": ["Wood", "Silicon", "Rubber", "Paper"],
                "answer": "Silicon"
            },
            {
                "question": "Which component opposes current flow?",
                "options": ["Resistor", "Battery", "LED", "Antenna"],
                "answer": "Resistor"
            },
            {
                "question": "How many terminals does a typical BJT have?",
                "options": ["One", "Two", "Three", "Four"],
                "answer": "Three"
            }
        ]
    },

    "bee": {
        "name": "BEE",
        "questions": [
            {
                "question": "What is the SI unit of electric current?",
                "options": ["Volt", "Ampere", "Ohm", "Watt"],
                "answer": "Ampere"
            },
            {
                "question": "Which law relates voltage, current and resistance?",
                "options": [
                    "Newton's Law", "Ohm's Law",
                    "Faraday's Law", "Hooke's Law"
                ],
                "answer": "Ohm's Law"
            },
            {
                "question": "What is the SI unit of electrical power?",
                "options": ["Joule", "Watt", "Coulomb", "Ohm"],
                "answer": "Watt"
            },
            {
                "question": "What is the formula for Ohm's law?",
                "options": ["V = IR", "P = I/R", "I = VR", "R = VI"],
                "answer": "V = IR"
            },
            {
                "question": "Which instrument measures electric current?",
                "options": ["Voltmeter", "Ammeter", "Thermometer", "Barometer"],
                "answer": "Ammeter"
            },
            {
                "question": "How is an ammeter connected?",
                "options": [
                    "In series", "In parallel",
                    "Across the battery only", "Not connected"
                ],
                "answer": "In series"
            },
            {
                "question": "How is a voltmeter connected across a component?",
                "options": [
                    "In series", "In parallel",
                    "Only to ground", "Without wires"
                ],
                "answer": "In parallel"
            },
            {
                "question": "Two 2-ohm resistors in series have what total resistance?",
                "options": ["1 ohm", "2 ohms", "4 ohms", "8 ohms"],
                "answer": "4 ohms"
            },
            {
                "question": "What is the standard AC mains frequency in Pakistan?",
                "options": ["25 Hz", "50 Hz", "100 Hz", "200 Hz"],
                "answer": "50 Hz"
            },
            {
                "question": "Which device converts electrical energy into mechanical energy?",
                "options": ["Generator", "Electric motor", "Transformer", "Fuse"],
                "answer": "Electric motor"
            }
        ]
    },

    "cald": {
        "name": "CALD",
        "questions": [
            {
                "question": "Which gate produces an output of 1 only when both inputs are 1?",
                "options": ["OR", "AND", "NOT", "XOR"],
                "answer": "AND"
            },
            {
                "question": "Which gate inverts its input?",
                "options": ["AND", "OR", "NOT", "XOR"],
                "answer": "NOT"
            }
        ]
    },

    "sda": {
        "name": "SDA",
        "questions": [
            {
                "question": "What does UML stand for?",
                "options": [
                    "Unified Modeling Language",
                    "Universal Machine Logic",
                    "User Model List",
                    "Unified Main Language"
                ],
                "answer": "Unified Modeling Language"
            },
            {
                "question": "Which diagram shows interactions between an actor and a system?",
                "options": [
                    "Class diagram",
                    "Use case diagram",
                    "Deployment diagram",
                    "Component diagram"
                ],
                "answer": "Use case diagram"
            }
        ]
    }
}


def prepare_questions(subject):
    # ARRAY: Store questions by index.
    question_array = Array()

    # QUEUE: Process questions in FIFO order.
    question_queue = Queue()

    for question in subjects[subject]["questions"]:
        question_queue.enqueue(question)

        # 2. Load user-added questions

    if os.path.exists("question.json"):

        with open("question.json","r") as file:

            user_questions = json.load(file)


        if subject in user_questions:

            for question in user_questions[subject]:

                question_queue.enqueue(question)

    # LINKED LIST: Connect questions as circular nodes.
    question_list = LinkedList()

    while not question_queue.is_empty():
        question = question_queue.dequeue()
        question_array.insert(question)
        question_list.insert(question)

    return question_array, question_list


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/quiz/<subject>", methods=["GET", "POST"])
def quiz(subject):
    if subject not in subjects:
        return redirect(url_for("home"))

    question_array, question_list = prepare_questions(subject)
    total = question_array.size()
    questions = question_array.display()

    # Start a new quiz
    if request.method == "GET":
        session["quiz_subject"] = subject
        session["question_index"] = 0
        session["answers"] = {}
        session["answer_history"] = []
        session.pop("score", None)
        session.pop("result_subject", None)

    # Prevent mixing different subjects
    elif session.get("quiz_subject") != subject:
        return redirect(url_for("quiz", subject=subject))


    index = session.get("question_index", 0)
    answers = session.get("answers", {})


    if request.method == "POST":
        selected = request.form.get("answer")
        action = request.form.get("action", "next")

        # Save answer for the current question

        # Save answer for the current question
        if selected is not None:
            answers[str(index)] = selected
            session["answers"] = answers

            # STACK: Save answer submission history
            answer_history = Stack()

            for item in session.get("answer_history", []):
                answer_history.push(item)

            answer_history.push({
                "question_index": index,
                "answer": selected
            })

            session["answer_history"] = answer_history.items


        if action == "previous":
            index = max(0, index - 1)
            session["question_index"] = index

        elif action == "next":
            # An answer is required before moving forward
            if selected is None:
                return redirect(url_for("quiz", subject=subject))

            if index < total - 1:
                index += 1
                session["question_index"] = index
            else:
                # Calculate score once, after final submission
                score = sum(
                    1 for i, question in enumerate(questions)
                    if answers.get(str(i)) == question["answer"]
                )

                session["score"] = score
                session["result_subject"] = subject
                return redirect(url_for("result", subject=subject))

    question = question_list.get(index)
    progress = round((index + 1) / total * 100)

    return render_template(
        "quiz.html",
        question=question,
        number=index + 1,
        total=total,
        progress=progress,
        subject_name=subjects[subject]["name"],
        selected_answer=answers.get(str(index))
    )

@app.route("/result/<subject>")
def result(subject):
    if subject not in subjects:
        return redirect(url_for("home"))

    if session.get("result_subject") != subject:
        return redirect(url_for("quiz", subject=subject))
    return render_template(
        "result.html",
        score=session.get("score", 0),
        total=len(subjects[subject]["questions"]),
        subject_name=subjects[subject]["name"]
    )

@app.route("/add_question", methods=["GET", "POST"])
def add_question():

    if request.method == "POST":

        filename = "question.json"

        subject = request.form["subject"]
        question = request.form["question"]

        option1 = request.form["option1"]
        option2 = request.form["option2"]
        option3 = request.form["option3"]
        option4 = request.form["option4"]

        options = [option1, option2, option3, option4]

        selected = request.form["answer"]

        # Store the actual answer text
        answer = {
            "option1": option1,
            "option2": option2,
            "option3": option3,
            "option4": option4
        }[selected]

        new_question = {
            "question": question,
            "options": options,
            "answer": answer
        }

        # Load existing data
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        # Initialize subjects if they don't exist
        if subject not in data:
            data[subject] = []

        # Add question
        data[subject].append(new_question)

        # Save JSON
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Question Saved Successfully!")

        return redirect(url_for("home"))

    # GET request
    return render_template("add_question.html")


if __name__ == "__main__":
    app.run(debug=True)
