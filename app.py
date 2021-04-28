"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, get_time_now
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.drop_all()
db.create_all()

app.config['SECRET_KEY'] = "passkey"
debug = DebugToolbarExtension(app)


@app.route('/')
def main():

    return redirect('/users')

@app.route('/users')
def list_users():
    """List users and add user form"""
    
    users = User.query.all()
    return render_template('main.html', users=users)

@app.route('/new', methods=['GET', 'POST'])
def add_user():
    """New User Form"""
    
    if request.method == 'POST':

        fName = request.form['f_name']
        lName = request.form['l_name']
        imgUrl = request.form['img_url']

        user = User(first_name=fName, last_name=lName, image_url=imgUrl)
        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{user.id}')
    else:

        return render_template('add_user_form.html')
    

@app.route('/users/<int:user_id>')
def user_page(user_id):
    """User page"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user.id)
    return render_template('user_page.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit User"""

    if request.method == 'GET':

        user = User.query.get_or_404(user_id)
        return render_template('user_edit_form.html')

    else:

        user = User.query.get_or_404(user_id)
        user.first_name = request.form['f_name']
        user.last_name = request.form['l_name']
        user.image_url = request.form['image_url']

        db.session.add(user)
        db.session.commit()

        return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """delete user"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    users = User.query.all()

    return render_template('main.html', users=users)
    
# POST ROUTES

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    """add new post"""

    if request.method == 'GET':

        user = User.query.get_or_404(user_id)
        return render_template('new_post.html', user=user)
    
    else:
        
        user = User.query.get_or_404(user_id)

        title = request.form['title']
        content = request.form['content']

        post = Post(title=title, content=content, user=user)
        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    """show post page"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template('post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """post edit page GET and POST"""

    if request.method == "GET":

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)
        return render_template('post_edit.html', post=post, user=user)

    else:

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)

        title = request.form['title']
        content = request.form['content']

        post.title = title
        post.content = content
        post.created_at = get_time_now()

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """delete post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user.id}')