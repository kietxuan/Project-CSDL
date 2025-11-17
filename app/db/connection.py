import mysql.connector
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

def get_db_connection():
    """Tạo kết nối tới CSDL MySQL và trả về object connection."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối CSDL: {err}")
        return None
