from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from models import User, Task
from forms import RegistrationForm, LoginForm, TaskForm
from app import db, bcrypt

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
@main_routes.route('/index')
def index():
    return render_template('index.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main_routes.login'))
    return render_template('register.html', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main_routes.tasks'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@main_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_routes.index'))

@main_routes.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(content=form.content.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('main_routes.tasks'))
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', form=form, tasks=tasks)
