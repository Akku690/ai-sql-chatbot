import sqlite3
conn = sqlite3.connect("company.db")
cur = conn.cursor()
# Create a simple "customers" and "orders" table
cur.execute('''
CREATE TABLE IF NOT EXISTS customers (
 id INTEGER PRIMARY KEY,
 name TEXT,
 city TEXT
)
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS orders (
 id INTEGER PRIMARY KEY,
 customer_id INTEGER,
 product TEXT,
 amount REAL,
 order_date TEXT,
 FOREIGN KEY (customer_id) REFERENCES customers (id)
)
''')
# Insert sample data
customers = [
 (1, "Rohan Mehta", "Ludhiana"),
 (2, "Sara Khan", "Delhi"),
 (3, "Aman Verma", "Mumbai"),
]
orders = [
 (1, 1, "Laptop", 55000, "2026-01-12"),
 (2, 1, "Mouse", 700, "2026-02-03"),
 (3, 2, "Phone", 22000, "2026-02-15"),
 (4, 3, "Keyboard", 1500, "2026-03-01"),
 (5, 2, "Laptop", 60000, "2026-03-10"),
]
cur.executemany("INSERT OR IGNORE INTO customers VALUES (?,?,?)", customers)
cur.executemany("INSERT OR IGNORE INTO orders VALUES (?,?,?,?,?)", orders)
conn.commit()
conn.close()
print("Database created: company.db")