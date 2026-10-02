from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)


def get_db_connection():
     conn = sqlite3.connect('tasks.db')
     conn.row_factory = sqlite3.Row
     return conn



def init_db():
    conn = get_db_connection()
    conn.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    done TEXT NOT NULL
                    );
                    """)
    conn.commit()
    conn.close()


init_db()




tasks = [
    {'id': 1, 'name' : 'goon', 'description' : 'porn', 'done' : False},
    {'id': 2, 'name' : 'eat', 'description' : 'bacon nigga cheese', 'done' : True}
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/api/tasks', methods=['POST'])
def add_task():
     data = request.get_json()
     name = data.get("name")
     done = data.get("done")
     conn = get_db_connection()
     cursor = conn.cursor()
     cursor.execute("INSERT INTO tasks (name, done) VALUES (?, ?)", (name, done))
     conn.commit()
     new_id = cursor.lastrowid
     conn.close()
     new_task = {
          'id' : new_id,
          'name' : name,
          'done': done
     }
     return jsonify({'message':'task added', 'task':new_task}), 201


@app.route('/api/tasks/<int:id>', methods = ["PUT"])
def update_task(id):

    task = next((t for t in tasks if t['id'] == id), None)

    if task is None:
        return jsonify({'error':'not found'}), 404


    choice = request.get_json()

    tasks[id]['name'] = choice.get('title', tasks[id]['name'])
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