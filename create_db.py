import pymysql

try:
    # Connect to MySQL server without selecting a specific database
    conn = pymysql.connect(host='localhost', user='root', password='Sakshi@yash2005')
    cursor = conn.cursor()
    
    # Create the database if it doesn't already exist
    cursor.execute('CREATE DATABASE IF NOT EXISTS PANCHAYAT;')
    print("Database 'PANCHAYAT' created successfully!")
    
    conn.close()
except Exception as e:
    print("Error:", e)
