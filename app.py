from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB create
def init_db():
    conn = sqlite3.connect('rooms.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            roomNo TEXT,
            capacity INTEGER,
            hasAC INTEGER,
            hasWashroom INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def index():
    conn = sqlite3.connect('rooms.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rooms")
    rooms = c.fetchall()
    conn.close()
    return render_template('index.html', rooms=rooms)

# ADD ROOM
@app.route('/add', methods=['GET','POST'])
def add_room():
    if request.method == 'POST':
        roomNo = request.form['roomNo']
        capacity = request.form['capacity']
        ac = 1 if request.form.get('ac') else 0
        washroom = 1 if request.form.get('washroom') else 0

        conn = sqlite3.connect('rooms.db')
        c = conn.cursor()
        c.execute("INSERT INTO rooms VALUES (?,?,?,?)",
                  (roomNo, capacity, ac, washroom))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_room.html')

# SEARCH ROOM
@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        capacity = request.form['capacity']
        ac = request.form.get('ac')
        washroom = request.form.get('washroom')

        conn = sqlite3.connect('rooms.db')
        c = conn.cursor()

        query = "SELECT * FROM rooms WHERE capacity >= ?"
        params = [capacity]

        if ac:
            query += " AND hasAC=1"
        if washroom:
            query += " AND hasWashroom=1"

        c.execute(query, params)
        rooms = c.fetchall()
        conn.close()

        return render_template('search.html', rooms=rooms)

    return render_template('search.html', rooms=None)

# ALLOCATE ROOM
@app.route('/allocate', methods=['POST'])
def allocate():
    roomNo = request.form['roomNo']

    conn = sqlite3.connect('rooms.db')
    c = conn.cursor()
    c.execute("DELETE FROM rooms WHERE roomNo=?", (roomNo,))
    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)