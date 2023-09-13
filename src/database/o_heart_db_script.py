import sqlite3

conn = sqlite3.connect('on_heart_db.db')
print("Opened database successfully")

conn.execute('CREATE TABLE customer (cust_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, password TEXT, city TEXT)')
print("customer Table created successfully")

conn.execute('CREATE TABLE admin (admin_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, password TEXT, city TEXT)')
print("admin Table created successfully")

conn.execute('CREATE TABLE doctor (doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, city TEXT, state TEXT, country TEXT, address TEXt, phone_no BIGINT)')
print("doctor Table created successfully")
conn.close()