from flask import Flask, render_template, request, Blueprint
from visit_db_queries import *
from forms import SearchForm, LoginForm
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomeRandomString'

csrf = CSRFProtect(app)


@app.route('/login')
def login():
    """
    Для странички логина
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        return 'Submitted'
    return render_template('login.html', form=form)


@app.route('/signup')
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        return 'Submitted'
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    return 'Logout'


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    При обращении к example.com/ выдаётся страница index.html,
    на которой будет показан remote_addr и информация о посещениях
    Request.remote_addr возвращает IP-адрес клиента
    """

    add_visit(request.remote_addr, str(request.user_agent))

    return render_template('index.html')


@app.route('/view_info', methods=['GET', 'POST'])
def view_info():
    return render_template('info.html')


@app.route('/info_database', methods=['GET', 'POST'])
def info_by_ip_date():
    form = SearchForm()
    if form.validate_on_submit():
        try:
            start_date = datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day,
                                  0, 0, 0, 0)
            end_date = datetime(form.end_date.data.year, form.end_date.data.month, form.start_date.data.day,
                                23, 59, 59, 999999)
        except TypeError:
            start_date, end_date = None, None
        visits = get_all_visits_by_ip_and_dates(str(form.ip.data), start_date, end_date)
        if len(visits) != 0:
            html_text = '<h2>From {0} to {1} for {2}</h2>'.format(str(start_date), str(end_date), str(form.ip.data))
            for visitor in visits:
                html_text += '<ul>UserAgent: {0}<br>DateTime: {1}</ul>'.format(visitor.user_agent, visitor.date_time)
            return html_text
    error_for_no_visits = 'No visits for this IP address'
    return render_template('info_by_ip_date.html', form=form, error_for_no_visits=error_for_no_visits)


@app.route('/info_ip_table', methods=['GET', 'POST'])
def info_ip_table():
    visits = get_all_visits()
    html_text = ''
    for visitor in visits:
        html_text += '<ul>IP address: {0}<br>Date visited: {1}<br>User Agent: {2}</ul>' \
            .format(visitor.ip_address, visitor.date_time, visitor.user_agent)
    return html_text


if __name__ == "__main__":
    create_visit_table()
    app.run(host='0.0.0.0', debug=True)
    visit_close_connection()
