from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from flask_fontawesome import FontAwesome
from secret import get_secret

secret = get_secret("all_cred")

app = Flask(__name__)
app.secret_key = 'flash message'
fa = FontAwesome(app)

# Update these with your Cloud SQL connection details
db_config = {
    'host': secret['host'],
    'database': secret['database'],
    'user': secret['user'],
    'password': secret['password']
}

def get_connection():
    return psycopg2.connect(**db_config)

@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    flash("Data Updated Successfully")

    id_data = request.form['id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET name=%s, email=%s, phone=%s
        WHERE id=%s
    """, (name, email, phone, id_data))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id_data>', methods=['GET'])
def delete(id_data):
    flash("Data Deleted Successfully")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
