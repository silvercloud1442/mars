from flask import Flask, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
import os
from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User
from data.RegisterForm import RegisterForm
from data.LoginForm import LoginForm
from data.JobsForm import JobsForm


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
global_init('db/dbase.sqlite')

@app.route('/')
@app.route('/index')
def index():
    session = create_session()
    jobs_list = []
    for jobs in session.query(Jobs).all():
        jobs_list.append(jobs)
    return render_template('index.html', jobs=jobs_list)


@app.route('/promotion')
def promo():
    countdown_list = ['Человечество вырастает из детства.',
                      'Человечеству мала одна планета.',
                      'Мы сделаем обитаемыми безжизненные пока планеты.',
                      'И начнем с Марса!',
                      'Присоединяйся!']
    return '</br>'.join(countdown_list)


@app.route('/image_mars')
def image():
    return '''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс</h1>
                  </body>
                    <img src="/static/img/mars.jpg" alt="здесь должна была быть картинка, но не нашлась">
                    <h3>Вот она какая, красная планета<h3>
                </html>'''


@app.route('/promotion_image')
def image_prom():
    return '''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Яндекс!</title>
                    <style>
                        h1{
                          color: #FF0000;
                          }
                        li{
                          list-style: none;
                          }
                        .gray{
                          background-color: #ccc0c0;
                          }
                        .green{
                          background-color: #83d982;
                          }
                        .yellow{
                          background-color: #d3d62b;
                          }
                        .red{
                          background-color: #c23838;
                          }
                    </style>
                  </head>
                  <body>
                    <h1>Жди нас, Марс</h1>
                  </body>
                    <img src="/static/img/mars.jpg" alt="здесь должна была быть картинка, но не нашлась">
                    <h3 class=shit><li class=gray>Человечество вырастает из детства.</li></br>
                      <li class=green>Человечеству мала одна планета.</li></br>
                      <li class=gray>Мы сделаем обитаемыми безжизненные пока планеты.</li></br>
                      <li class=yellow>И начнем с Марса!</li></br>
                      <li class=red>Присоединяйся!</li></br><h3>
                </html>'''


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            id=len(session.query(User).all()) + 1,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            addres=form.addres.data,
            email=form.email.data,
        )
        pas = form.password.data
        user.hassed_password = User.set_password(pas)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = JobsForm()
    if form.validate_on_submit():
        session = create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('jobs.html', title='Adding a job',
                           form=form)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
