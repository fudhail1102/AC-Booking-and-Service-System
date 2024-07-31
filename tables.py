import mysql.connector as msc
from dotenv import load_dotenv
import os

def create_tables():
    # Load environment variables from the .env file
    load_dotenv()

    # Get the environment variables
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    # Connect to the MySQL server (without specifying the database)
    mycon = msc.connect(
        host=db_host,
        user=db_user,
        passwd=db_password
    )

    # Create a cursor object
    cursor = mycon.cursor()

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    # Select the database
    cursor.execute(f"USE {db_name}")

    # Create the tables
    cursor.execute("CREATE TABLE IF NOT EXISTS customers (name VARCHAR(255), username VARCHAR(255), password VARCHAR(255), mobileno INT, address VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS products (model_id VARCHAR(10) NOT NULL, brand VARCHAR(20) NOT NULL, price INT NOT NULL, ac_type VARCHAR(30) NOT NULL, ac_system VARCHAR(20) NOT NULL, power_rating VARCHAR(20))")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id VARCHAR(10) NOT NULL, model_id VARCHAR(10) NOT NULL, name VARCHAR(100) NOT NULL, address VARCHAR(255) NOT NULL, mobile_no BIGINT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS services (booking_id VARCHAR(10) NOT NULL, type VARCHAR(20) NOT NULL, service VARCHAR(20) NOT NULL, name VARCHAR(100) NOT NULL, address VARCHAR(255) NOT NULL, mobileno BIGINT NOT NULL)")

    # Insert data into the products table from the file
    with open("productstableinsertion.txt", "r") as f:
        insertlist = f.readlines()

    insertlist1 = [i.strip() for i in insertlist]  # Remove newline characters

    for j in insertlist1:
        query = f"INSERT INTO products (brand, ac_type, ac_system, power_rating, price, model_id) VALUES {j}"
        cursor.execute(query)

    mycon.commit()  # Commit the transaction

    # Close the connection
    mycon.close()
