from flask import Flask, url_for, render_template
from data.db_session import global_init, create_session
from data.jobs import Jobs

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    global_init('db/dbase.sqlite')
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
