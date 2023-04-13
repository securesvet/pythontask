from flask import Flask, render_template, request, redirect, url_for
from visit_db_queries import *
from forms import SearchForm, IpDateForm, IpForm, DateForm, UserAgentForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomeRandomString'

csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    При обращении к example.com/ выдаётся страница index.html,
    на которой будет показан remote_addr и информация о посещениях
    Request.remote_addr возвращает IP-адрес клиента
    """
    current_ip_addr = request.remote_addr
    current_user_agent = request.user_agent

    add_visit(current_ip_addr, str(current_user_agent))

    return render_template('index.html')


@app.route('/view_info', methods=['GET', 'POST'])
def view_info():
    return render_template('info.html')


@app.route('/info_by_date', methods=['GET', 'POST'])
def info_by_date():
    form = DateForm()
    if form.validate_on_submit():
        start_date = datetime.combine(form.start_date.data, datetime.min.time())
        end_date = datetime.combine(form.end_date.data, datetime.min.time())
        visits = get_all_ip_by_dates(start_date, end_date)
        if len(visits) != 0:
            html_text = '<h2>From {0} to {1}</h2>'.format(str(start_date), str(end_date))
            for visitor in visits:
                html_text += '<ul>IP address: {0}<br>UserAgent: {1}<br>DateTime: {2}</ul>'.format(visitor.ip_address,
                                                                                                  visitor.user_agent,
                                                                                                  visitor.date_time)
            return html_text
    return render_template('info_by_date.html', form=form)


@app.route('/info_by_browser', methods=['GET', 'POST'])
def info_by_browser():
    form = UserAgentForm()
    return render_template('info_by_browser.html', form=form)


@app.route('/info_by_ip', methods=['GET', 'POST'])
def info_by_ip():
    form = IpForm()
    try:
        if form.validate_on_submit():
            ip_address = form.ip.data
            list_of_visitor = get_all_visits_by_ip(ip_address)
            if len(list_of_visitor) != 0:
                html_text = '<h1>Query for {0}'.format(ip_address)
                for visitor in list_of_visitor:
                    html_text += '<ul>Date visited: {0}<br>User Agent: {1}</ul>'.format(visitor.date_time, visitor.user_agent)
                return html_text
    except DoesNotExist:
        return "<h1>No such IP</h1>"
    return render_template('info_by_ip.html', form=form)


@app.route('/info_by_ip_date', methods=['GET', 'POST'])
def info_by_ip_date():
    form = IpDateForm()
    if form.validate_on_submit():
        start_date = datetime.combine(form.start_date.data, datetime.min.time())
        end_date = datetime.combine(form.end_date.data, datetime.min.time())
        visits = get_all_visits_by_ip_and_dates(str(form.ip.data), start_date, end_date)
        if len(visits) != 0:
            html_text = '<h2>From {0} to {1} for {2}</h2>'.format(str(start_date), str(end_date), str(form.ip.data))
            for visitor in visits:
                html_text += '<ul>UserAgent: {0}<br>DateTime: {1}</ul>'.format(visitor.user_agent, visitor.date_time)
            return html_text
    return render_template('info_by_ip_date.html', form=form)


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
    app.run(host='0.0.0.0')
    visit_close_connection()
