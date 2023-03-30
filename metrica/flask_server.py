from flask import Flask, render_template, request
from handle import check_for_user_agent_in_file

app = Flask(__name__)

menu = ['Посещений всего']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        user_agent = request.headers.get('User-Agent')
        check_for_user_agent_in_file(str(user_agent), 'counting.txt')
    return render_template('index.html', menu=menu)


if __name__ == "__main__":
    # По дефолту на 127.0.0.1:5000
    app.run(debug=True)
