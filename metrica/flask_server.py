from flask import Flask, render_template, request
from visit_db_queries import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_my_ip() -> str:
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
    print(get_all_ip_by_date(datetime(2023,4,12)))
    print('all visit today between 22 and 23')
    print(get_all_ip_by_dates(datetime(2023,4,12,22), datetime(2023,4,12,23)))


    return render_template('index.html')
    # return render_template('index.html', remote_ip_addr=current_ip_addr, count_overall=get_counts_overall(),
    #                        count_unique_today=get_today_unique_visits(), count_unique=get_unique_visits(),
    #                        count_today_overall=get_today_overall_visits())


if __name__ == "__main__":
    create_visit_table()
    app.run(host='0.0.0.0', debug=True)
    visit_close_connection()
