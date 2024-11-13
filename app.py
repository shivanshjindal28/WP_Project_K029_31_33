from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database connection
conn = psycopg2.connect("dbname=expense_tracker user=shivansh password=shivansh")

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Analysis page route
@app.route('/analysis')
def analysis():
    # Optionally, fetch some data from the database if needed
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT 5")
        recent_transactions = cur.fetchall()
    return render_template('analysis.html', transactions=recent_transactions)

# Accounts page route
@app.route('/accounts')
def accounts():
    # Optionally, you can fetch account-related data
    return render_template('accounts.html')

# More page route
@app.route('/more')
def more():
    # Optionally, fetch more details if needed
    return render_template('more.html')

# Adding transaction route
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    type = data.get('type')
    category = data.get('category')

    print("START Backend")
    print(user_id)
    print(amount)
    print(type)
    print(category)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO transactions (user_id, amount, type, category) VALUES (%s, %s, %s, %s) RETURNING *",
            (user_id, amount, type, category)
        )
        conn.commit()
        transaction = cur.fetchone()
        return jsonify(transaction)

# Fetch recent transactions route
@app.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY date DESC LIMIT 5", (user_id,))
        transactions = cur.fetchall()
        return jsonify(transactions)
    
@app.route('/transactions/type/<transaction_type>', methods=['GET'])
def get_transactions_type(transaction_type):
    print("Getting called type")
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM transactions WHERE type = %s", (transaction_type,))
        transactions = cur.fetchall()
        return jsonify(transactions)

if __name__ == "__main__":
    app.run(debug=True)
