from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session

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
    if not is_select:
        mydb.commit()  # Commit changes for non-SELECT queries
    if is_select:
        result = cursor.fetchall()  # Fetch result for SELECT queries
        return result

# Create customer table
def create_customers_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database to validate email and password
        query = 'SELECT * FROM customers WHERE email = %s AND password = %s'
        result = db_query(query, (email, password), is_select=True)
        
        if result:
            # Save user info in session
            session['user_id'] = result[0][9]  # Store the account number (user_id)
            session['username'] = result[0][0]  # Store the username
            return redirect(url_for('view_customers'))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route('/view_customers')
def view_customers():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    query = 'SELECT * FROM customers'
    customers = db_query(query, is_select=True)
    return render_template('view_customers.html', customers=customers)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
