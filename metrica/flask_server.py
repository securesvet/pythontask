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

    all_visits = get_all_visits()
    # for visit in all_visits:
    #     print(visit.ip_address, visit.user_agent, visit.datetime)


    return render_template('index.html')
    # return render_template('index.html', remote_ip_addr=current_ip_addr, count_overall=get_counts_overall(),
    #                        count_unique_today=get_today_unique_visits(), count_unique=get_unique_visits(),
    #                        count_today_overall=get_today_overall_visits())


if __name__ == "__main__":
    create_visit_table()
    app.run(host='0.0.0.0', debug=True)
    visit_close_connection()
