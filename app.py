from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = 'expenses.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    total = conn.execute('SELECT SUM(price) FROM expenses').fetchone()[0] or 0.0

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    weekly_total = conn.execute(
        'SELECT SUM(price) FROM expenses WHERE date >= ?',
        (start_of_week.strftime('%Y-%m-%d'),)
    ).fetchone()[0] or 0.0

    monthly_total = conn.execute(
        'SELECT SUM(price) FROM expenses WHERE date >= ?',
        (start_of_month.strftime('%Y-%m-%d'),)
    ).fetchone()[0] or 0.0

    yearly_total = conn.execute(
        'SELECT SUM(price) FROM expenses WHERE date >= ?',
        (start_of_year.strftime('%Y-%m-%d'),)
    ).fetchone()[0] or 0.0

    category_data = conn.execute('SELECT category, SUM(price) as total FROM expenses GROUP BY category').fetchall()
    categories = [row['category'] for row in category_data]
    values = [row['total'] for row in category_data]

    conn.close()

    return render_template('index.html',
                           expenses=expenses,
                           total=total,
                           weekly_total=weekly_total,
                           monthly_total=monthly_total,
                           yearly_total=yearly_total,
                           labels=categories,
                           data=values)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        price = float(request.form['price'])

        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (date, description, category, price) VALUES (?, ?, ?, ?)',
                     (date, description, category, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
