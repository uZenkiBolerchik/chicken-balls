from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    return render_template('index.html')


@app.route('/api/task/<id>', methods=['GET'])
def task():
    task_id = request.args.get('user_task_id')
    return render_template(f'task{task_id}.html')
