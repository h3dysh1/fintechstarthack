from flask import Flask, render_template

app = Flask(__name__)

# Sample data for lessons and quizzes
lessons = [
    {"title": "Home Loans", "content": "Information about home loans..."},
    {"title": "HECS", "content": "Information about HECS..."}
]

quizzes = [
    {"title": "Home Loans Quiz", "questions": [
        {"question": "What is a mortgage?", "options": ["A type of loan", "A savings account"], "answer": "A type of loan"},
        {"question": "What is HECS?", "options": ["A home loan", "A student loan"], "answer": "A student loan"}
    ]}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lessons')
def lessons():
    return render_template('lessons.html', lessons=lessons)

@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html', quizzes=quizzes)

if __name__ == '__main__':
    app.run(debug=True)
