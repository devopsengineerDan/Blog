from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField,RadioField,TextAreaField,IntegerField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from app.models import Users,Posts,Comments


class Post(FlaskForm):
   '''
   Blog post form.
   '''
   title = StringField('Post', validators=[DataRequired(),Length(min=2,max=140)], render_kw={"placeholder": "Title"})
   content = TextAreaField('Content', render_kw={"placeholder": "Article Content"})
   picture =  FileField('Blog Post Image', validators=[FileAllowed(['png','jpg','jpeg'])], render_kw={"placeholder": "Image"})
   submit = SubmitField('Publish')

   def validate_username(self,title):

      post = Posts.query.filter_by(title=title.data).first()
      if post:
         raise ValidationError('A post with that title already exists. Mind coming up with something unique.')

class Comment(FlaskForm):
   '''
   Comment form.
   '''
   name = StringField('Name', validators=[DataRequired(),Length(min=2,max=200)], render_kw={"placeholder": "Enter your name"})
   comment = TextAreaField('Comment', validators=[DataRequired(),Length(min=2,max=200)], render_kw={"placeholder": "Have thoughts on the article?"})
   commented_on = IntegerField('Post Id')
   submit = SubmitField('Send')


class Bio(FlaskForm):
   '''
   Update bio.
   '''
   bio = TextAreaField('Bio', validators=[DataRequired()], render_kw={"placeholder": "Write something about yourself"})
   submit = SubmitField('Update Bio')

class Subscribe(FlaskForm):
   '''
   Subscription form
   '''

   email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
   submit = SubmitField('Subscribe')