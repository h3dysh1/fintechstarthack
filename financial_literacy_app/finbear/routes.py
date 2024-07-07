from flask import render_template, url_for, flash, redirect, request
from finbear import app, db, bcrypt, login_manager
from finbear.forms import RegistrationForm, LoginForm
from finbear.models import User
from flask_login import login_user, current_user, login_required, logout_user


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

@app.route('/register', methods=["GET", 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/lessons')
def lessons():
    return render_template('lessons.html', lessons=lessons_data)

@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html', quizzes=quizzes_data)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    answer1 = request.form.get('question1')
    answer2 = request.form.get('question2')
    
    # Define correct answers
    correct_answers = {
        'question1': 'A loan for purchasing a house',
        'question2': 'Higher Education Contribution Scheme'
    }

    # Initialise score
    score = 0
    if answer1.strip().lower() == correct_answers['question1'].strip().lower():
        score += 1
    if answer2.strip().lower() == correct_answers['question2'].strip().lower():
        score += 1

    return render_template('quiz_result.html', score=score)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
