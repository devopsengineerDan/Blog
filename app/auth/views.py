from flask import render_template,redirect,url_for,flash,request
from . import auth
from .. import db,bcrypt
from .forms import SignUp,LogIn
from ..models import Users
from flask_login import login_user,logout_user,login_required


@auth.route('/', methods=['GET','POST'])
def signup():
   title = 'Sign Up'
   signup_form = SignUp()
   if signup_form.validate_on_submit():
         hashed_pass = bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8')
         user = Users(name = signup_form.name.data, username = signup_form.username.data, email = signup_form.email.data, password = hashed_pass)
         db.session.add(user)
         db.session.commit()
         return redirect(url_for('auth.login'))

         flash(f'Account successfully created for {signup_form.username.data}')

   return render_template('auth/signup.html', signup = signup_form, title = title)


@auth.route('/login', methods=['GET','POST'])
def login():
   title = 'Log In'
   login_form = LogIn()
   if login_form.validate_on_submit():
      user = Users.query.filter_by(username = login_form.username.data).first()
      if user is not None and bcrypt.check_password_hash(user.password, login_form.password.data):
         login_user(user,login_form.remember_me.data)
         return redirect(request.args.get('next') or url_for('main.write'))

   return render_template('auth/login.html', login = login_form, title = title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))   