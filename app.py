"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag, get_time_now
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
    elif request.method == 'GET':

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

    #User.query.filter_by(id=user_id).delete()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    users = User.query.all()

    return redirect('/users')
    
# POST ROUTES

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    """add new post"""

    if request.method == 'GET':

        user = User.query.get_or_404(user_id)
        tags = Tag.query.all()
        return render_template('new_post.html', user=user, tags=tags)
    
    else:
        
        user = User.query.get_or_404(user_id)

        title = request.form['title']
        content = request.form['content']
        tag_ids = [int(id) for id in request.form.getlist('tags')]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        post = Post(title=title, content=content, user=user, tags=tags)
        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    """show post page"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = post.tags
    return render_template('post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """post edit page GET and POST"""

    if request.method == "GET":

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)
        tags = Tag.query.all()
        content = post.content

        return render_template('post_edit.html', post=post, user=user, tags=tags, content=content)

    else:

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)

        title = request.form['title']
        content = request.form['content']
        tag_ids = [int(id) for id in request.form.getlist('tags')]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        post.title = title
        post.content = content
        post.created_at = get_time_now()
        post.tags = tags

        db.session.add(post)
        db.session.commit()

        return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """delete post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/tags')
def get_tags():
    """show all tags"""

    tags = Tag.query.all()

    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """show tag details"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new', methods=['GET', 'POST'])
def new_tag():
    """New Tag form"""

    if request.method == 'POST':

        tagName = request.form['tag_name']

        tag = Tag(name=tagName)
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

    elif request.method == 'GET':

        return render_template('create_tag.html')

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit Tag"""

    if request.method == 'GET':

        tag = Tag.query.get_or_404(tag_id)

        return render_template('edit_tag.html', tag=tag)
    
    elif request.method == 'POST':

        tag = Tag.query.get_or_404(tag_id)

        tagName = request.form['tag_name']

        tag.name = tagName
        
        db.session.commit()

        return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    tags = Tag.query.all()

    return redirect('/tags')
    