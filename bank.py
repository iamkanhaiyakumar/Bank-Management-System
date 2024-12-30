from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Establishing connection to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Iamkk0104@",
    database="bank"
)

cursor = mydb.cursor()

# Function to query the database
def db_query(query, values=None, is_select=False):
    cursor.execute(query, values)
    if is_select:
        # For SELECT queries, we fetch results
        result = cursor.fetchall()
        return result
    else:
        # For non-SELECT queries (INSERT/UPDATE/DELETE), we commit changes
        mydb.commit()

# Create customer table
def create_customers_table():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    username VARCHAR(20),
                    password VARCHAR(20),
                    name VARCHAR(20),
                    email VARCHAR(50) UNIQUE,
                    age INTEGER,
                    contact VARCHAR(15),
                    address TEXT,
                    city VARCHAR(20),
                    balance INTEGER,
                    account_number INTEGER PRIMARY KEY AUTO_INCREMENT,
                    status BOOLEAN)
    ''')
    mydb.commit()

create_customers_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve data from the form
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        contact = request.form['contact']
        address = request.form['address']
        city = request.form['city']
        balance = request.form['balance']
        
        # Insert the data into the database
        query = '''INSERT INTO customers (username, password, name, email, age, contact, address, city, balance, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        values = (username, password, name, email, int(age), contact, address, city, int(balance), True)
        db_query(query, values)
        
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/view_customers')
def view_customers():
    query = 'SELECT * FROM customers'
    customers = db_query(query, is_select=True)  # Fetching results for SELECT query
    return render_template('view_customers.html', customers=customers)

if __name__ == "__main__":
    app.run(debug=True)
