from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin@123')")
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']

#     # Vulnerable SQL query with string concatenation
#     query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
#     result = cursor.execute(query).fetchone()

#     if result:
#         return f"Welcome, {result[1]}!"
#     else:
#         return "Invalid credentials"
    
@app.route('/login', methods=['POST'])
def login_secure():
    username = request.form['username']
    password = request.form['password']

    # Use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    result = cursor.execute(query, (username, password)).fetchone()

    if result:
        return f"Welcome, {result[1]}!"
    else:
        return "Invalid credentials"


if __name__ == '__main__':
    app.run(debug=True)
