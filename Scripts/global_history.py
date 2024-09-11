import mysql.connector
import logging
import os

# Ensure the log directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging for store_data.py
logging.basicConfig(
    filename='logs/main.log',  # Log file path
    level=logging.INFO,              # Log level (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MySQLDatabase:
    def __init__(self, host='localhost', user='root', password='Santosh032', database='popular_searches'):
        self.host = host
        self.user = user
        self.password = 'Santosh032'
        self.database = database
        self.conn = None

    def connect(self):
        """Establishes the connection to the MySQL database."""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logging.info("Successfully connected to the MySQL database.")
        except mysql.connector.Error as err:
            logging.error(f"MySQL connection error: {err}")
            self.conn = None

    def close(self):
        """Closes the connection to the database."""
        if self.conn:
            self.conn.close()
            logging.info("MySQL connection closed.")

    def store_search_term(self, search_term):
        """Stores the search term in the global_history table or updates its count if it already exists."""
        if not self.conn:
            logging.error("No database connection.")
            return False

        try:
            cursor = self.conn.cursor(dictionary=True)

            # Check if the search term already exists
            cursor.execute("""
                SELECT search, search_count
                FROM global_history
                WHERE search = %s
            """, (search_term,))
            existing_search = cursor.fetchone()

            if existing_search:
                # If the search term exists, increment the search count
                new_count = existing_search['search_count'] + 1
                cursor.execute("""
                    UPDATE global_history
                    SET search_count = %s
                    WHERE search = %s
                """, (new_count, search_term))
                logging.info(f"Search term '{search_term}' updated with count {new_count}.")
            else:
                # If the search term doesn't exist, insert it with count = 1
                cursor.execute("""
                    INSERT INTO global_history (search, search_count)
                    VALUES (%s, %s)
                """, (search_term, 1))
                logging.info(f"New search term '{search_term}' inserted with count 1.")

            self.conn.commit()
            return True

        except Exception as e:
            logging.error(f"Error storing search term: {e}")
            return False

# Class to handle the insertion of data
class StoreData:
    def __init__(self, search_term):
        self.search_term = search_term
        self.db = MySQLDatabase()

    def execute(self):
        """Handles the connection to the database and stores the search term."""
        self.db.connect()
        if self.db.conn:
            success = self.db.store_search_term(self.search_term)
            if success:
                logging.info(f"Successfully stored or updated search term: {self.search_term}")
            else:
                logging.error(f"Failed to store search term: {self.search_term}")
            self.db.close()
        else:
            logging.error("Could not connect to the MySQL database.")

# if __name__ == "__main__":
#     # Example usage
#     search_term = "flask"  # Replace this with the search term you want to store
#     store_instance = StoreData(search_term)
#     store_instance.execute()
