from flask import render_template, request, redirect, url_for
from app import app, db
# from app.models import Post
from app.models import Post,User
# Define the Post model (in models.py, explained below)

@app.route('/')
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('feed'))
    return render_template('add_user.html')

@app.route('/user_posts/<int:user_id>')
def user_posts(user_id):
    user = User.query.get(user_id)
    posts = user.posts
    return render_template('user_posts.html', user=user, posts=posts)
@app.route('/feed')
def feed():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)


@app.route('/create_post', methods=['POST'])
def create_post():
    if request.method == 'POST':
        print( request.method)
        content = request.form['content']
        user_id = request.form['user_id']  # Get user_id from the form
        # Check if the user with the given user_id exists
        print(user_id,content)
        user = User.query.get(user_id)
        print(user)
        if user:
            post = Post(content=content, author=user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('feed'))
        else:
            # Handle the case where the user does not exist.
            flash('User not found.', 'danger')  # You can use Flask's flash messages here.
            return redirect(url_for('feed'))
      
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.content = request.form['post_content']
        db.session.commit()
        return redirect(url_for('feed'))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('feed'))

