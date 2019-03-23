from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from app.models import Users

class SignUp(FlaskForm):
   '''
   Creates the form for registration
   '''
   name = StringField('Name', validators=[DataRequired(),Length(min=2)], render_kw={"placeholder": "Enter Your Full Name"})
   username = StringField('Username', validators=[DataRequired(),Length(min=2,max=13)], render_kw={"placeholder": "Username"})
   email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
   password = PasswordField('Password', validators=[DataRequired(),Length(min=8)], render_kw={"placeholder": "Password"})
   confirm_password = PasswordField('Password', validators=[DataRequired(),Length(min=8), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
   submit = SubmitField('Sign Up')

   def validate_username(self,username):

      user = Users.query.filter_by(username=username.data).first()
      if user:
         raise ValidationError('That username is already taken!')

   def validate_email(self,email):

      user = Users.query.filter_by(email=email.data).first()
      if user:
         raise ValidationError('An account with that email already exists.')


class LogIn(FlaskForm): 
   '''
   Creates log in form
   '''
   username = StringField('Username', validators=[DataRequired(),Length(min=2,max=13)], render_kw={"placeholder": "Username"})
   password = PasswordField('Password', validators=[DataRequired(),Length(min=8)], render_kw={"placeholder": "Password"})
   remember_me = BooleanField('Remember Me')
   submit = SubmitField('Log In')