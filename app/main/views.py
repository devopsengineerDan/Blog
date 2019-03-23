import os
import secrets
import re
from app.request import get_quotes
from flask import render_template,redirect,url_for,flash,request,abort
from . import main
from sqlalchemy import desc
from flask_login import login_required,current_user
from .. import db,mail
from flask_mail import Message
from ..models import Users,Posts,Comments,Subscriptions
from flask_login import login_user
from .forms import Post,Comment,Bio,Subscribe
from ..request import get_quotes
import markdown2


@main.route('/', methods=['GET','POST'])
def index():
   title = 'Welcome'
   quote_obj = get_quotes()
   user_login_status = current_user.is_authenticated

   sub_form = Subscribe()

   if sub_form.validate_on_submit():
      subscription = Subscriptions(email = sub_form.email.data)

      if subscription is not None:
         subscription.save_sub()

      return (redirect(url_for('main.index')))
      
      flash('You\'ve successfully subscribed to this blog')

   quote = quote_obj['quote']
   quote_author = quote_obj['author']

   post = Posts.query.order_by(desc(Posts.time)).all()
    
   return render_template('landing.html', title= title, posts = post, user = current_user, quote = quote, quote_author = quote_author, status = user_login_status, sub = sub_form) 


@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
   title =  current_user.name
   user_login_status = current_user.is_authenticated

   posts = Posts.query.filter_by(author = current_user).order_by(desc(Posts.time)).all()

   return render_template('profile.html', title= title, user = current_user, posts = posts, status = user_login_status)

def save_picture(picture):
   random_name = secrets.token_hex(8)
   _, f_ext = os.path.splitext(picture.filename)
   image_filename = random_name + f_ext
   picture_path = os.path.join(app.instance_path, 'static/images/blog_images', image_filename)
   picture.save(picture_path)

   return image_filename


@main.route('/recent-posts', methods=['GET','POST'])
def posts():
   title = 'Recent Posts'
   user_login_status = current_user.is_authenticated

   sub_form = Subscribe()

   if sub_form.validate_on_submit():
      subscription = Subscriptions(email = sub_form.email.data)

      if subscription is not None:
         subscription.save_sub()

      return (redirect(url_for('main.posts')))

      flash('You\'ve successfully subscribed to this blog')

      


   post = Posts.query.order_by(desc(Posts.time)).all()
    
   return render_template('posts.html', title= title, posts = post, user = current_user, status = user_login_status, sub = sub_form) 
   

@main.route('/write', methods=['GET','POST'])
@login_required
def write():
   title =  'New Blog Post'
   avatar = f'avatars/{current_user.avatar}'

   user_login_status = current_user.is_authenticated

   post_form = Post()



   if post_form.validate_on_submit():
      if post_form.picture.data:
         picture = save_picture(post_form.picture.data)
      else:
         picture = 'post.jpg'

      post_link = re.sub(r'\s', '-', post_form.title.data).lower()
      post = Posts(title = post_form.title.data, content = post_form.content.data, image = picture, author = current_user, link = post_link)
      
      if post is not None:
         post.save_post()

      flash('You have successfully published your article')

      subscriptions = Subscriptions.query.all()
      if subscriptions:
         
         for sub in subscriptions:
            msg = Message(subject="New Blog Post",
                           sender="chumbadev@gmail.com",
                           recipients=[sub.email],
                           body=f'A new post has been published by {current_user.name}. Check it out.')
            mail.send(msg)

      return (redirect(url_for('main.read', article_link=post_link)))

   return render_template('new.html', title= title, post = post_form, user = current_user, avatar = avatar, status = user_login_status)

@main.route('/read/<article_link>', methods=['GET', 'POST'])
def read(article_link):

   comment_form = Comment()

   art_link = str(article_link)

   post = Posts.get_post(art_link)

   converted = markdown2.markdown(post.content,extras=["code-friendly", "fenced-code-blocks"])

   title = post.title

   sub_form = Subscribe()

   if sub_form.validate_on_submit():
      subscription = Subscriptions(email = sub_form.email.data)

      if subscription is not None:
         subscription.save_sub()

      return (redirect(url_for('main.read', article_link=art_link)))

      flash('You\'ve successfully subscribed to this blog')

   user_login_status = current_user.is_authenticated

   if comment_form.validate_on_submit():
      comment =  Comments(name = comment_form.name.data, comment = comment_form.comment.data, posted_on = comment_form.commented_on.data)

      if comment is not None:
         comment.save_comment()

      return (redirect(url_for('main.read', article_link=article_link)))


   return render_template('read.html', title = title, user = current_user, post = post, comment = comment_form, status = user_login_status, sub = sub_form, content = converted)


@main.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update_blog(id):

   post = Posts.query.get_or_404(id)

   form = Post()

   title = f'Update Post | {post.title}'

   if form.validate_on_submit():
      post.title = form.title.data
      post.content = form.content.data
      db.session.commit()
      flash('You\'ve successfully updated your blog post')

      return (redirect(url_for('main.read', article_link=post.link)))
   elif request.method == 'GET':
      form.title.data = post.title
      form.content.data = post.content

   user_login_status = current_user.is_authenticated

   return render_template('update.html', title = title, user = current_user, post = post, form = form, status = user_login_status)

@main.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_blog(id):

   post = Posts.query.filter_by(id = id).first()

   post.delete_post()

   return (redirect(url_for('main.profile')))


@main.route('/comment/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_comment(id):

   comment = Comments.query.filter_by(id = id).first()

   comment.delete_comment()

   post = Posts.query.filter_by(id = comment.posted_on).first()

   flash('Comment has been deleted!')

   return (redirect(url_for('main.read', article_link=post.link)))