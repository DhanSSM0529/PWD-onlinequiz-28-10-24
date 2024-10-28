from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_questions():
    with open('questions.json') as f:
        questions = json.load(f)
    return questions

@app.route('/')
def quiz():
    questions = load_questions()
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    questions = load_questions()

    feedback = []
    correct_answers = 0

    for q in questions:
        question_id = str(q['id'])
        user_answer = data.get(question_id)
        correct_answer = q['answer']
        explanation = q['explanation']
        
        is_correct = (user_answer == correct_answer)
        if is_correct:
            correct_answers += 1
        
        feedback.append({
            "id": question_id,
            "question": q['question'],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": explanation
        })

    total_questions = len(questions)
    return jsonify({"score": correct_answers, "total": total_questions, "feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)

