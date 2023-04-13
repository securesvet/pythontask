from flask import Flask, render_template, request, redirect, url_for
from visit_db_queries import *
from forms import SearchForm
from flask_wtf.csrf import CSRFProtect
import os

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
    header = request.headers

    add_visit(str(header))

    print("IP-address connected: " + current_ip_addr)

    print('all ip')
    print(get_all_ip())
    print('all visits by current id')
    print(get_all_visits_by_ip(current_ip_addr))
    print('all visits today')
    print(get_all_ip_by_date(datetime(2023, 4, 12)))
    print('all visit today between 22 and 23')
    print(get_all_ip_by_dates(datetime(2023, 4, 12, 22), datetime(2023, 4, 12, 23)))
    form = SearchForm()
    return render_template('index.html', form=form)


@app.route('/view_info', methods=['GET', 'POST'])
def view_info():
    # form = SearchForm()
    # if form.validate_on_submit():
    #     ip_data = str(form.ip.data)
    #     start_date_data = str(form.start_date.data)
    #     end_date_data = str(form.end_date.data)
    #     text_h2 = '<h2> Info about {0} on dates from: {1} to {2}'.format(ip_data, start_date_data, end_date_data)
    #     text = '<ul><li>' + str(form.ip.data) + '</li></ul>'
    #     return text_h2
    return render_template('info.html')


@app.route('/info_by_date', methods=['GET', 'POST'])
def info_by_date():
    form = SearchForm()
    if form.validate_on_submit():
        start_date_data = str(form.start_date.data)
        end_date_data = str(form.end_date.data)
        return '<h2>From {0} to {1}</h2>'.format(start_date_data, end_date_data)
    return render_template('info_by_date.html', form=form)


@app.route('/info_by_browser', methods=['GET', 'POST'])
def info_by_browser():
    form = SearchForm()
    return render_template('info_by_browser.html', form=form)


@app.route('/info_by_ip', methods=['GET', 'POST'])
def info_by_ip():
    form = SearchForm()
    if form.validate_on_submit():
        ip_address = form.ip.data
        return '<h1>Query for {0}'.format(ip_address)
    return render_template('info_by_ip.html', form=form)


@app.route('/info_by_ip_date', methods=['GET', 'POST'])
def info_by_ip_date():
    form = SearchForm()
    if form.validate_on_submit():
        ip_address = form.ip.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        return '<h1>Query for {0} from {1} to {2}</h1>'.format(ip_address, start_date, end_date)
    return render_template('info_by_ip_date.html', form=form)


@app.route('/info_ip_table', methods=['GET', 'POST'])
def info_ip_table():
    return render_template('info_ip_table.html')


if __name__ == "__main__":
    create_visit_table()
    app.run(host='0.0.0.0', debug=True)
    visit_close_connection()
