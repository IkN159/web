from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import app, db
from .models import Category, News, User
from .forms import get_categories, NewsForm, RegistrationForm, LoginForm

@app.route("/")
def home_page():
    news_lst = News.query.order_by(News.created_date.desc()).all()
    categories = Category.query.all()
    return render_template("index.html", lst_news=news_lst, categories=categories)

@app.route("/category/<int:id>")
def category_news(id):
    category = Category.query.get_or_404(id)
    news_list = category.news
    categories = Category.query.all()
    return render_template("category.html", category=category, news_list=news_list, categories=categories)

@app.route("/news_detail/<int:id>")
def news_detail(id):
    one_news = News.query.get_or_404(id)
    categories = Category.query.all()
    return render_template("news_detail.html", news=one_news, categories=categories)

@app.route("/registration/", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Регистрация прошла успешно! Теперь войдите.", "success")
        return redirect(url_for("login"))
    return render_template("registration.html", form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"С возвращением, {user.name}!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for("home_page"))
        else:
            flash("Неверное имя пользователя или пароль.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("login"))

@app.route("/add_news", methods=["GET", "POST"])
@login_required
def add_news():
    form = NewsForm()
    form.category.choices = get_categories()
    if form.validate_on_submit():
        category = Category.query.get(form.category.data)
        new_news = News(...)
        db.session.add(new_news)
        db.session.commit()
        flash("Новость успешно добавлена!", "success")
        return redirect(url_for("news_detail", id=new_news.id))
    return render_template("add_news.html", form=form)