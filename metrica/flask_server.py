from flask import Flask, render_template, request
from handle import check_for_user_agent_in_file, counting_all_visit, counting_all_unique_visitor

app = Flask(__name__)

filename = 'counting.txt'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        user_agent = request.headers.get('User-Agent')
        check_for_user_agent_in_file(str(user_agent), filename)
        count_of_visitors_alltime = counting_all_visit(filename)
        count_unique_visitors = counting_all_unique_visitor(filename)

    return render_template('index.html', count_overall=count_of_visitors_alltime, count_unique=count_unique_visitors)


if __name__ == "__main__":
    # По дефолту на 127.0.0.1:5000
    app.run(debug=True)
