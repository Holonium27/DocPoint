import sqlite3
conn=sqlite3.connect("project.db")
cur=conn.cursor()
query1=""" CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    speciality TEXT NOT NULL, 
    address TEXT NOT NULL
)"""
cur.execute(query1)

query2="""CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT

)"""
cur.execute(query2)

query3="""CREATE TABLE slots (
    doctor_id INTEGER ,
    name TEXT,
    day INTEGER,
    slot1 BOOL,
    slot2 BOOL,
    slot3 BOOL,
    slot4 BOOL,
    slot5 BOOL,
    slot6 BOOL,
    slot7 BOOL,
    slot8 BOOL,
    slot9 BOOL,
    slot10 BOOL,
    FOREIGN KEY (doctor_id) references doctors (id)
)"""
cur.execute(query3)

query4="""CREATE TABLE appointments (
     count INTEGER
 )"""
cur.execute(query4)