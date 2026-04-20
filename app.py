from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("event.db")

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS registrations (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, event_id INTEGER)")
    conn.commit()
    conn.close()
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

    return render_template("success.html", message="✅ User Added Successfully!")

@app.route("/add_event", methods=["POST"])
def add_event():
    event_name = request.form["event_name"]
    date = request.form["date"]
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO events (event_name, date) VALUES (?, ?)", (event_name, date))
    conn.commit()
    conn.close()

    return render_template("success.html", message="✅ Event Added Successfully!")

@app.route("/register", methods=["POST"])
def register():
    user_id = request.form["user_id"]
    event_id = request.form["event_id"]
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO registrations (user_id, event_id) VALUES (?, ?)", (user_id, event_id))
    conn.commit()
    conn.close()

    return render_template("success.html", message="✅ Registration Successful!")

@app.route("/participants")
def participants():
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT users.name, events.event_name FROM registrations  
              JOIN users ON users.id = registrations.user_id
              JOIN events ON events.id = registrations.event_id""")
    data = c.fetchall()
    conn.close()

    return render_template("participants.html", data=data)

@app.route("/update_user", methods=["POST"])
def update_user():
    user_id = request.form["user_id"]
    name = request.form["name"]
    email = request.form["email"]
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
    conn.commit()
    conn.close()

    return render_template("success.html", message="✏️ User Updated Successfully!")

@app.route("/update_event", methods=["POST"])
def update_event():
    event_id = request.form["event_id"]
    event_name = request.form["event_name"]
    date = request.form["date"]
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE events SET event_name=?, date=? WHERE id=?", (event_name, date, event_id))
    conn.commit()
    conn.close()

    return render_template("success.html", message="✏️ Event Updated Successfully!")

@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_id = request.form["user_id"]
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return render_template("success.html", message="🗑️ User Deleted Successfully!")

@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_id = request.form["event_id"]
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()

    return render_template("success.html", message="🗑️ Event Deleted Successfully!")

if __name__ == "__main__":
    app.run(debug=True)