from flask import render_template, url_for, flash, redirect, request
from finbear import app, db, bcrypt
from finbear.forms import RegistrationForm, LoginForm
from finbear.models import User, QuizScore
from flask_login import login_user, current_user, login_required, logout_user

# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    db.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

# Sample data for lessons and quizzes
lessons_data = [
    {"title": "Home Loans", "content": "Information about home loans..."},
    {"title": "HECS", "content": "Information about HECS..."}
]

quizzes_data = [
    {"title": "Home Loans Quiz", "questions": [
        {"question": "What is a mortgage?", "options": ["A type of loan", "A savings account"], "answer": "A type of loan"},
        {"question": "What is HECS?", "options": ["A home loan", "A student loan"], "answer": "A student loan"}
    ]}
]


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.create(username=form.username.data, email=form.email.data, password=hashed_password)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(email=form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/lessons')
def lessons():
    return render_template('lessons.html', lessons=lessons_data)

@app.route('/quizzes')
def quizzes():
    print(current_user)
    return render_template('quizzes.html', quizzes=quizzes_data)

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    answer1 = request.form.get('question1').strip().lower()
    answer2 = request.form.get('question2').strip().lower()
    
    # Define correct answers
    correct_answers = {
        'question1': 'A loan for purchasing a house',
        'question2': 'Higher Education Contribution Scheme'
    }

    # Initialise score
    score = 0
    if answer1 == correct_answers['question1'].strip().lower():
        score += 1
    if answer2 == correct_answers['question2'].strip().lower():
        score += 1
    quiz_score = QuizScore.get_or_none(user=current_user)
    if quiz_score:
        quiz_score.update(score=score).execute()
    else:
        QuizScore.create(score=score, user=current_user)
    return render_template('quiz_result.html', score=score)

