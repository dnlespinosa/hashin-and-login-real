from django.shortcuts import render
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Tweet
from forms import UserForm, TweetForm
from sqlalchemy.exc import IntegrityError

app=Flash(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
app.config['SECRET_KEY'] = 'Sup Anh'

connect_db(app)

def salting_hash(phrase, salt=None):
    if salt is None:
        salt = str(randint(1000,9999))
        
    hashed = slightly_better_hash(f'{phrase}{salt}')
    return f'{hashed}{salt}'

app.route('/')
def home_page():
    return redirect('register.html')

app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_pwd = salting_hash(pwd)

        user = User.register(username, new_pwd)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)

app.route('/login')
def login_user():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        new_pwd = salting_hash(pwd)

        user = User.authenticate(username, new_pwd)

        if user:
            session['user_id'] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ['WRONG MOVE']
    return render_template('login.html', form=form)


@app.route('/secret')
def secret():
    if 'user_id' not in session:
        flash('you must be logged in')
        return redirect('/')
    else:
        flash('YOU MADE IT')
        return render_template('secret.html')

    
@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')

    

