import re

from flask import Flask, render_template, request, make_response, Response
from visit_db_queries import *
from forms import SearchForm, LoginForm, SignUpForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomeRandomString'

csrf = CSRFProtect(app)


def create_cookies_response_index(username: str, max_age: int = 60 * 60 * 24 * 365 * 2) -> Response:
    response = make_response(render_template('index.html', count_of_visits_by_ip=get_count_of_ip_visits(),
                                             count_of_all_visits=get_count_of_all_visits(),
                                             count_of_auth=get_count_of_auth()))
    response.set_cookie('username', username, max_age)
    return response


def is_valid_ip(ip_address: str) -> bool:
    """
    Функция возвращает значение True, если переданный хост валидный,
    и возвращает False, если нет
    :param ip_address:
    :return:
    """
    # Паттерн для айпи адреса
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][' \
              r'0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip_address))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Для странички логина
    :return:
    """
    form = LoginForm()

    if form.validate_on_submit():
        if does_username_exist(form.username.data) and get_password(form.username.data) == form.password.data:

            return create_cookies_response_index(form.username.data)
        else:
            return 'Wrong username or password!'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if not does_username_exist(form.username.data):
            if form.password.data == form.re_password.data:
                add_new_user(form.username.data, form.password.data)
                return create_cookies_response_index(form.username.data)
        else:
            return 'User already exists'
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    res = make_response(render_template('index.html'))
    res.set_cookie('username', 'None', max_age=0)
    return create_cookies_response_index('', 0)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    При обращении к example.com/ выдаётся страница index.html,
    на которой будет показан remote_addr и информация о посещениях
    Request.remote_addr возвращает IP-адрес клиента
    """

    add_visit(request.remote_addr, str(request.user_agent))

    return render_template('index.html', count_of_visits_by_ip=get_count_of_ip_visits(),
                           count_of_all_visits=get_count_of_all_visits(), count_of_auth=get_count_of_auth())


@app.route('/view_info', methods=['GET', 'POST'])
def view_info():
    return render_template('info.html')


@app.route('/info_database', methods=['GET', 'POST'])
def info_by_ip_date():
    form = SearchForm()
    if form.is_submitted():
        if is_valid_ip(form.ip.data):
            try:
                start_date = datetime(form.start_date.data.year, form.start_date.data.month, form.start_date.data.day,
                                      0, 0, 0, 0)
                end_date = datetime(form.end_date.data.year, form.end_date.data.month, form.end_date.data.day,
                                    23, 59, 59, 999999)
                visits = get_all_visits_by_ip_and_dates(str(form.ip.data), start_date, end_date)
            except AttributeError:
                start_date, end_date = None, None
                visits = get_all_visits_by_ip_and_dates(str(form.ip.data))
            if len(visits) != 0:
                if start_date and end_date:
                    html_text = '<h2>From {0} to {1}, for {2}</h2>'.format(str(start_date), str(end_date), str(form.ip.data))
                elif start_date:
                    html_text = '<h2>From {0} for {1}</h2>'.format(str(start_date), str(form.ip.data))
                elif end_date:
                    html_text = '<h2>From very beginning to {0}, for {1}</h2>'.format(str(end_date), str(form.ip.data))
                else:
                    html_text = '<h2>For all time</h2>'

                for visitor in visits:
                    html_text += '<ul>UserAgent: {0}<br>DateTime: {1}</ul>'.format(visitor.user_agent, visitor.date_time)
                return html_text
        else:
            return 'IP is not valid'
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
