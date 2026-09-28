from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


tasks = [
    {'id': 1, 'name' : 'goon', 'description' : 'porn', 'done' : False},
    {'id': 2, 'name' : 'eat', 'description' : 'bacon nigga cheese', 'done' : True}
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route('/api/tasks/<int:id>', methods = ["PUT"])
def update_task(id):

    task = next((t for t in tasks if t['id'] == id), None)

    if task is None:
        return jsonify({'error':'not found'}), 404


    choice = request.get_json()

    tasks[id]['name'] = choice.get('title', tasks[id]['name'])
    tasks[id]['description'] = choice.get('description', tasks[id]['description'])
    tasks[id]['done'] = choice.get('done', tasks[id]['done'])

    return jsonify({'message': 'Updated', 'task': tasks[id]}), 200

@app.route('/api/tasks/<int:id>', methods = ['DELETE'])
def delete_task(id):
    if id not in tasks:
            return jsonify({'error':'not found'}), 404

    choice = request.get.json()

    tasks.remove(tasks[id])
    return jsonify({'message':'deleted'}), 200




if __name__ == '__main__':
    app.run(debug=True)