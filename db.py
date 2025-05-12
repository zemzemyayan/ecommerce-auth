# db.py
import mysql.connector
from config import MYSQL_CONFIG

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)


def get_user_by_id(user_id):
    """Verilen user_id ile kullanıcıyı MySQL veritabanından al."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()  # Bir kullanıcıyı al
    cursor.close()
    connection.close()
    return user