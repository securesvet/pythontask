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
    if request.method == 'GET':
        current_ip_addr = request.remote_addr
        add_visit(current_ip_addr)
        get_table()
        print(current_ip_addr)
        return render_template('index.html', remote_ip_addr=current_ip_addr, count_overall=get_counts_overall(),
                               count_unique_today=get_today_unique_visits(), count_unique=get_unique_visits())
    return "GET method was not used"


if __name__ == "__main__":
    create_visit_table()
    app.run(host='0.0.0.0')
    visit_close_connection()
