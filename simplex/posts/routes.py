from flask import render_template, flash, redirect, url_for, abort, Markup, Blueprint, Markup
from flask_login import login_required, current_user

from simplex import app, db
from simplex.posts.models import Post
from simplex.posts.forms import PostNewFrom
from simplex.utils import save_image

import markdown, os

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostNewFrom()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        if form.img_file.data:
            pic_file = save_image(form.img_file.data)
            post.img_file = pic_file
        db.session.add(post)
        db.session.commit()
        flash('Gönderi oluşturuldu', 'success')
        return redirect(url_for('main.home'))
    return render_template('posts/post_create.html', title='Yeni Gönderi', form=form)

@posts.route('/post/<int:post_id>')
def detail_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.content = Markup(markdown.markdown(post.content))
    return render_template('posts/post_detail.html', post=post, title=post.title)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostNewFrom()
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        if form.img_file.data:
            if post.img_file != 'default.jpg':
                delete_pics = os.path.join(app.root_path, 'static', 'post_pics', post.img_file)
                os.remove(delete_pics)  # old pic deleted
            pic_file = save_image(form.img_file.data, _type='post')
            post.img_file = pic_file
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()
        flash('Gönderi güncellendi','success')
        return redirect(url_for('main.home'))
    form.title.data = post.title
    form.content.data = post.content

    return render_template('posts/post_update.html', post=post, form=form)

@posts.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if post.img_file != 'default.jpg':
        os.remove(os.path.join(app.root_path, 'static', 'post_pics', post.img_file))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home'))
