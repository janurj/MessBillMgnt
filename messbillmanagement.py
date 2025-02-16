  import mysql.connector
from mysql.connector import errorcode

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jananir40@",
            database="messbillmanagement"
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        return None

# Function to record a profit or loss entry
def record_profit_loss(connection):
    cursor = connection.cursor()

    # Get input from the user
    transaction_date = input("Enter transaction date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))  # Convert input to float
    entry_type = input("Enter type (Income or Expense): ").capitalize()  # Convert input to title case

    # Insert data into the ProfitLoss table
    insert_query = """
    INSERT INTO ProfitLoss (transaction_date, description, amount, type)
    VALUES (%s, %s, %s, %s)
    """

    data = (transaction_date, description, amount, entry_type)

    try:
        cursor.execute(insert_query, data)
        connection.commit()
        print("Entry recorded successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()

# Function to calculate and display total profit and total loss
def calculate_and_display_totals(connection):
    cursor = connection.cursor()

    # Calculate total profit
    cursor.execute("SELECT SUM(amount) FROM ProfitLoss WHERE type = 'Profit'")
    total_profit = cursor.fetchone()[0] or 0

    # Calculate total loss
    cursor.execute("SELECT SUM(amount) FROM ProfitLoss WHERE type = 'Loss'")
    total_loss = cursor.fetchone()[0] or 0

    print(f"Total Profit: {total_profit}")
    print(f"Total Loss: {total_loss}")

    cursor.close()

# Main function
def main():
    connection = connect_to_database()

    if connection:
        # Example: Record a profit or loss entry
        record_profit_loss(connection)

        # Calculate and display totals
        calculate_and_display_totals(connection)

        # Close the database connection
        connection.close()

if __name__ == "__main__":
    main()
