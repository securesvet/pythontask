from flask import Flask, render_template, request, jsonify
from visit_db import *

app = Flask(__name__)

'''
При обращении к example.com/ выдаётся страница index.html,
на которой будет показан remote_addr и информация о посещениях
Request.remote_addr возвращает ip-адрес клиента
'''


@app.route('/', methods=['GET'])
def get_my_ip():
    if request.method == 'GET':
        current_ip_addr = request.remote_addr
        add_visit(current_ip_addr)
        get_table()
        print(current_ip_addr)
        count_visits, today_visit, last_day_visit = get_count_info_by_ip(current_ip_addr)
        return render_template('index.html', remote_ip_addr=current_ip_addr, count_overall=count_visits, count_unique=0)
    return jsonify({'something wrong'})


if __name__ == "__main__":
    # По дефолту на 127.0.0.1:5000
    # Работает во внутренней сети
    app.run(host='0.0.0.0')
