from simplex import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    img_file = db.Column(db.String(80), default='default.jpg')

    def __repr__(self):
        return f'<Post {self.title}:{self.date_posted}>'
