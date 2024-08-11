from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'mysql_db'),
    user=os.getenv('MYSQL_USER', 'todo_user'),
    password=os.getenv('MYSQL_PASSWORD', 'password'),
    database=os.getenv('MYSQL_DATABASE', 'todo_db')
)
cursor = db.cursor()

# Create table with status column if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        status ENUM('Not Started', 'Started', 'Done') DEFAULT 'Not Started',
        completed BOOLEAN NOT NULL DEFAULT FALSE
    )
''')
cursor.execute('DROP TABLE IF EXISTS todos')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        status ENUM('Not Started', 'Started', 'Done') DEFAULT 'Not Started',
        completed BOOLEAN NOT NULL DEFAULT FALSE
    )
''')


@app.route('/')
def index():
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    status = request.form.get('status', 'Not Started')
    if task:
        cursor.execute("INSERT INTO todos (task, status) VALUES (%s, %s)", (task, status))
        db.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>', methods=['POST'])
def update_status(todo_id):
    new_status = request.form['status']
    cursor.execute("UPDATE todos SET status = %s WHERE id = %s", (new_status, todo_id))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    cursor.execute("DELETE FROM todos")
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
