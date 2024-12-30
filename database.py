#Database Management Banking
import mysql.connector 



mydb = mysql.connector.connect(
    host="localhost",  # Closing quote added here
    user="root",       # Correct order of arguments
    password="Iamkk0104@",  # Corrected syntax
    database="bank"  # Add this if a specific database is required
)


cursor = mydb.cursor()

def db_query(str):
    cursor.execute(str)
    result = cursor.fetchall()
    return result

def createcustomertable():
   cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        username VARCHAR(20) NOT NULL,
        password VARCHAR(20) NOT NULL,
        name VARCHAR(50),
        email VARCHAR(50) UNIQUE,
        age TINYINT UNSIGNED,
        city VARCHAR(50),
        balance DECIMAL(10, 2),
        account_number BIGINT UNSIGNED AUTO_INCREMENT,
        status BOOLEAN,
        PRIMARY KEY (account_number)
    )
''')


mydb.commit()

if __name__ == "__main__":
    createcustomertable()