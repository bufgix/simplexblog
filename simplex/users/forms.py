from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, EqualTo, ValidationError

from simplex.users.models import User

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı adı', validators=[DataRequired()])
    password = PasswordField("Sifre", validators=[DataRequired()])
    confirm_password= PasswordField("Sifre tekrar", validators=[DataRequired(), EqualTo('password',message='Aynı şifreleri girin')])
    secret_key = PasswordField('Gizli Anahtar', validators=[DataRequired(message='Bu alanı doldurun')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Kullanıcı adı alınmış', 'danger')
            raise ValidationError("<username> is taken")

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı adı', validators=[DataRequired()])
    password = PasswordField('Sifre', validators=[DataRequired()])
    remember = BooleanField('Beni hatırla')
    submit = SubmitField('Giriş Yap')

class UpdateAccountForm(FlaskForm):
    motto = StringField('İmza', default='Standart Üye')
    img_file = FileField('Profil Resmi', validators=[FileAllowed(['png', 'jpg', 'gif'], message="Sadece (.png, .jpg, .gif) dosyalarını yükleyebilirsiniz.")])
    submit = SubmitField('Güncelle')
