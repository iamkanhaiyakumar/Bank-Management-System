#Database Management Banking
import mysql.connector 



mydb = mysql.connector.connect(
    host="localhost",  # Closing quote added here
    user="root",       # Correct order of arguments
    password="Iamkk0104@",  # Corrected syntax
    database="bank"  # Add this if a specific database is required
)


cursor = mydb.cursor()

def db_query(query, values=None, is_select=False):
    cursor.execute(query, values)
    if not is_select:
        mydb.commit()  # Commit changes for non-SELECT queries
    if is_select:
        result = cursor.fetchall()  # Fetch result for SELECT queries
        return result
    
def createcustomertable():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers
                (username VARCHAR(20),
                password VARCHAR(20),
                name varchar(20),
                email VARCHAR(50) UNIQUE,
                age INTEGER,
                contact VARCHAR(15),
                address TEXT,
                city VARCHAR(20),
                balance INTEGER,
                account_number INTEGER,
                status BOOLEAN)
    ''')

mydb.commit()

if __name__ == "__main__":
    createcustomertable()