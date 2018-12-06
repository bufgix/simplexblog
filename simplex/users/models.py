from simplex import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    img_file = db.Column(db.String(80), default='default.jpg')
    motto = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"<User {self.username}: {self.img_file}>"
