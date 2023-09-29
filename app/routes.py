from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Post

# Define the Post model (in models.py, explained below)

@app.route('/')
@app.route('/feed')
def feed():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)

@app.route('/create_post', methods=['POST'])
def create_post():
    post_content = request.form['post_content']
    post = Post(content=post_content)
    db.session.add(post)
    db.session.commit()
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
