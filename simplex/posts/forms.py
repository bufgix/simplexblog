from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, EqualTo, ValidationError

class PostNewFrom(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    img_file = FileField('Thumnail', validators=[FileAllowed(['png', 'jpeg', 'jpg'], message="Sadece (.png, .jpg, .jpeg) dosyalarını yükleyebilirsiniz.")])
    submit = SubmitField('Yayımla')
