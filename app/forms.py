from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo

from .models import Category

def get_categories():
    return [(c.id, c.title) for c in Category.query.all()]

class NewsForm(FlaskForm):
    title = StringField("Название", validators=[
        DataRequired(message="Поле не должно быть пустым"),
        Length(max=255, message="Заголовок не может превышать 256 символов")
    ])
    text = TextAreaField("Текст новости", validators=[
        DataRequired(message="Поле не должно быть пустым")
    ])
    category = SelectField("Категория", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Добавить")

class LoginForm(FlaskForm):
    username = StringField("Имя пользователя:", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")

class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя:", validators=[DataRequired()])
    name = StringField("Введите имя:", validators=[DataRequired()])
    email = StringField("Введите Email адрес:", validators=[DataRequired(), Email(message="Некорректный Email адрес.")])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    password2 = PasswordField("Подтвердите пароль:", validators=[DataRequired(), EqualTo("password", message="Пароли не совпадают.")])
    submit = SubmitField("Зарегистрироваться")