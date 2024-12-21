from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .utils import hash_password, verify_password
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # verifico si el usuario existe por su email
        user = User.query.filter_by(email=email).first()

        # verifico si existe
        if user:
            # verifico si el password es igual al de la base
            if verify_password(user.password, password):
                flash('Logged in seccessfully!', category='success')
                # registro en la variable de session
                login_user(user, remember=True)
                # redirect to home
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect user or password, try again.', category='error')
        else:
            flash('Incorrect user or password, try again.', category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required # Indica que debe estar logueado para acceder a esta parte
def logout():
    # Elimino la session del usuario actual
    logout_user()
    # Redirijo al login jejej
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4 :
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 4:
            flash('Name must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:

            # verifico si el usuario existe por su email
            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email exited, can you try with another email.', category='error')
            else:
                # add user to database
                password=hash_password(password1)
                #password = password1
                new_user = User(email=email, name=name, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!.', category='success')
                # redirect to home
                return redirect(url_for('views.dashboard'))

    return render_template("register.html", user=current_user)
