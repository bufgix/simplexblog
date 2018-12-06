from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from simplex import app, db, bcrypt
from simplex.users.models import User
from simplex.posts.models import Post
from simplex.users.forms import LoginForm, RegisterForm, UpdateAccountForm
from simplex.utils import save_image



users = Blueprint('users', __name__)


@users.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.secret_key.data != app.secret_key:
            flash('Yöneticiden anahtar isteyin', 'danger')
        else:
            user = User(username=form.username.data, password=bcrypt.generate_password_hash(form.password.data), motto='Standart Üye')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Başarıyla kayıt oldunuz", "success")
            return redirect(url_for('main.home'))
    return render_template('users/register.html', form=form, title='Kayıt ol')

@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #login
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Başarıyla giriş yaptınız', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Hatalı kullanıcı adı veya şifre', 'danger')

    return render_template('users/login.html', form=form, title='Giriş')


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.img_file.data:
            if current_user.img_file != 'default.jpg':
                delete_pics = os.path.join(app.root_path, 'static', 'profile_pics', current_user.img_file)
                os.remove(delete_pics)  # old pic deleted
            pic_file = save_image(form.img_file.data, _type='profile')
            current_user.img_file = pic_file
        current_user.motto = form.motto.data
        db.session.commit()
        flash('Bilgiler güncellendi', 'success')
    elif request.method == 'GET':
        form.motto.data = current_user.motto

    page = request.args.get('page', 1, type=int)
    user_posts = Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=6)
    user_names = [name[0] for name in db.session.query(User.username).all()]
    return  render_template('users/account.html', title=f' {current_user.username} profili', form=form, posts=user_posts, user_names=user_names)

@users.route('/user/<username>')
def profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    ## HARD CODE ALERT FİX İT
    user_posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=6)



    return render_template('users/profile.html', posts=user_posts, user=user)

@users.route('/logout')
def logout():
    logout_user()
    next_page = request.args.get('next')
    flash('Başarıyla çıkış yaptınız', 'success')
    return redirect(next_page) if next_page else redirect(url_for('main.home'))
