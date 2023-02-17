from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = '21f1000072'


@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


# Login page (the decks will be s aved on your account)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query = """SELECT * FROM users WHERE username=? AND password=?"""
        cur.execute(query, (username, password))
        rows = cur.fetchall()

        if len(rows) == 1:
            # set session
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')


# If login fails, you'll have to register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        try:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            conn = sqlite3.connect("project.db")
            cur = conn.cursor()
            query = """INSERT INTO users (name,username,password) VALUES (?,?,?)"""
            cur.execute(query, (name, username, password))
            conn.commit()

            if cur.rowcount == 1:
                return redirect(url_for('index'))
            else:
                return "Username already exists <a href='/register'>Try Register again</a>"
        except:
            return "Something went wrong"

    return render_template('register.html')


@app.route('/')
def index():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    query1 = """SELECT COUNT(id) FROM DOCTORS"""
    cur.execute(query1)
    number1 = cur.fetchone()[0]
    query2 = """SELECT COUNT(id) FROM USERS"""
    cur.execute(query2)
    number2 = cur.fetchone()[0]
    query3 = """SELECT count FROM appointments"""
    cur.execute(query3)
    number3 = cur.fetchone()[0]
    return render_template('home.html', doctors=number1, users=number2, appointments=number3)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contactus')
def contactus():
    return render_template('contact.html')


@app.route('/email')
def email():
    return redirect("http://www.gmail.com")


@app.route('/search')
def search():
    return render_template('search.html')


def getname(l):
    copy = []  # To make a list of lists instead of list of tuples
    for o in l:
        for i in o:
            j = list(i)
            copy.append(j)

    copy_copy = copy

    for i in range(len(copy)):
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query = """SELECT name FROM DOCTORS WHERE id = ? """
        cur.execute(query, (copy[i][0],))
        n = cur.fetchone()[0]

        copy_copy[i][0] = n
    return copy_copy


@app.route('/appointments')
def appointments():
    appointments = []
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    query = """SELECT doctor_id,day,1 FROM slots WHERE slot1 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,2 FROM slots WHERE slot2 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,3 FROM slots WHERE slot3 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,4 FROM slots WHERE slot4 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,5 FROM slots WHERE slot5 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,6 FROM slots WHERE slot6 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,7 FROM slots WHERE slot7 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,8 FROM slots WHERE slot8 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,9 FROM slots WHERE slot9 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)
    query = """SELECT doctor_id,day,10 FROM slots WHERE slot10 = 'TRUE' """
    cur.execute(query)
    rows = cur.fetchall()
    if rows != []:
        appointments.append(rows)

    l = getname(appointments)
    num = len(l)
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    query1 = """UPDATE appointments SET count = ? """
    cur.execute(query1, (num,))
    conn.commit()
    return render_template('appointments.html', rows=l)


@app.route('/search/speciality', methods=['GET', 'POST'])
def speciality():
    if request.method == "POST":
        speciality = request.form['dname']
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query = """SELECT * FROM DOCTORS WHERE speciality = ? """
        cur.execute(query, (speciality,))
        rows = cur.fetchall()

        return render_template('load_doctors.html', rows=rows)
    return render_template('speciality.html')


@app.route('/search/name', methods=['GET', 'POST'])
def name():
    if request.method == "POST":
        name = request.form['name']
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query = """SELECT * FROM DOCTORS WHERE name = ? """
        cur.execute(query, (name,))
        rows = cur.fetchall()

        return render_template('load_doctors.html', rows=rows)
    return render_template('name.html')


@app.route('/search/location', methods=['GET', 'POST'])
def location():
    if request.method == "POST":
        loc = request.form['loc']
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query = """SELECT * FROM DOCTORS WHERE address = ? """
        cur.execute(query, (loc,))
        rows = cur.fetchall()

        return render_template('load_doctors.html', rows=rows)
    return render_template('location.html')


@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    query = """SELECT * FROM DOCTORS"""
    cur.execute(query)
    rows = cur.fetchall()
    return render_template("doctors.html", rows=rows)


@app.route('/book/<name>', methods=['GET', 'POST'])
def book_1(name):
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()

    query1 = """SELECT id FROM DOCTORS WHERE name = ?"""
    cur.execute(query1, (name,))
    id = cur.fetchone()[0]

    query2 = """SELECT day FROM slots WHERE doctor_id = ?"""
    cur.execute(query2, (id,))
    rows = cur.fetchall()
    days = []
    for row in rows:
        for day in row:
            days.append(day)

    if request.method == "POST":
        day = request.form['day']
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query1 = """SELECT id FROM DOCTORS WHERE name = ?"""
        cur.execute(query1, (name,))
        id = cur.fetchone()[0]
        return redirect(url_for('book_2', name=name, id=id, day=day))
    return render_template("book_1.html", name=name, rows=days)


@app.route('/book/<name>/<id>/<day>', methods=['GET', 'POST'])
def book_2(name, id, day):

    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    query2 = """SELECT * FROM slots WHERE doctor_id = ? AND day = ? """
    cur.execute(query2, (id, day,))
    row = cur.fetchone()
    slots = []
    for i in range(len(row)):
        if i > 1:
            if row[i] == "FALSE":
                slots.append(i-1)

    if request.method == "POST":
        slot = request.form['slot']
        print(name, id, day, slot)
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        if slot == '1':
            query1 = """UPDATE slots SET slot1 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query1, (day, id,))
            conn.commit()
        elif slot == '2':
            query2 = """UPDATE slots SET slot2 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query2, (day, id,))
            conn.commit()
        elif slot == '3':
            query3 = """UPDATE slots SET slot3 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query3, (day, id,))
            conn.commit()
        elif slot == '4':
            query4 = """UPDATE slots SET slot4 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query4, (day, id,))
            conn.commit()
        elif slot == '5':
            query5 = """UPDATE slots SET slot5 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query5, (day, id,))
            conn.commit()
        elif slot == '6':
            query6 = """UPDATE slots SET slot6 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query6, (day, id,))
            conn.commit()
        elif slot == '7':
            query7 = """UPDATE slots SET slot7 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query7, (day, id,))
            conn.commit()
        elif slot == '8':
            query8 = """UPDATE slots SET slot8 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query8, (day, id,))
            conn.commit()
        elif slot == '9':
            query9 = """UPDATE slots SET slot9 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query9, (day, id,))
            conn.commit()
        elif slot == '10':
            query10 = """UPDATE slots SET slot10 = 'TRUE' WHERE day = ? AND doctor_id = ? """
            cur.execute(query10, (day, id,))
            conn.commit()
        conn.close()
        return render_template("congratulations_booking.html", name=name, day=day, slot=slot)
    return render_template("book_2.html", name=name, day=day, rows=slots)


@app.route('/doctor-form', methods=['GET', 'POST'])
def doctor_form():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['address']
        speciality = request.form['speciality']
        fals = "FALSE"
        conn = sqlite3.connect("project.db")
        cur = conn.cursor()
        query1 = """INSERT INTO DOCTORS (name,speciality,address) VALUES (?,?,?)"""
        cur.execute(query1, (name, speciality, address))
        query2 = """SELECT id FROM DOCTORS WHERE name = ?"""
        cur.execute(query2, (name,))
        id = cur.fetchone()[0]
        query3 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query3, (id, 1, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query4 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query4, (id, 2, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query5 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query5, (id, 3, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query6 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query6, (id, 4, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query7 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query7, (id, 5, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query8 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query8, (id, 6, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query9 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query9, (id, 7, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query10 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query10, (id, 8, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query11 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query11, (id, 9, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        query12 = """INSERT INTO slots (doctor_id,day,slot1,slot2,slot3,slot4,slot5,slot6,slot7,slot8,slot9,slot10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
        cur.execute(query12, (id, 10, fals, fals, fals, fals,fals, fals, fals, fals, fals, fals))
        conn.commit()
        conn.close()
        return render_template('congratulations.html')
    return render_template('doctor_form.html')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5500)
