import sqlite3

conn = sqlite3.connect('expenses.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);
''')

conn.commit()
conn.close()

print("✅ Database and table created successfully.")
