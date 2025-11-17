from app.db.connection import get_db_connection
import mysql.connector

def get_all_doctors():
    """
    Lấy danh sách tất cả bác sĩ.
    Sắp xếp theo tên (A-Z) để dễ tìm kiếm trên giao diện.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Doctors ORDER BY DoctorName ASC")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []

def get_doctor_by_id(doctor_id):
    """
    Lấy thông tin chi tiết của 1 bác sĩ theo ID.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Doctors WHERE DoctorID = %s", (doctor_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return None

def create_doctor(name, specialty):
    """
    Thêm mới một bác sĩ.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Doctors (DoctorName, Specialty) VALUES (%s, %s)"
            cursor.execute(sql, (name, specialty))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return False

def update_doctor(doctor_id, name, specialty):
    """
    Cập nhật thông tin bác sĩ (Tên và Chuyên khoa).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE Doctors SET DoctorName = %s, Specialty = %s WHERE DoctorID = %s"
            cursor.execute(sql, (name, specialty, doctor_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return False

def delete_doctor(doctor_id):
    """
    Xóa bác sĩ.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Doctors WHERE DoctorID = %s", (doctor_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa bác sĩ (có thể do ràng buộc dữ liệu): {err}")
            return False
    return False

def search_doctors(keyword):
    """
    Tìm kiếm bác sĩ theo Tên hoặc Chuyên khoa.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            search_term = f"%{keyword}%"
            # Tìm kiếm cả trong tên HOẶC trong chuyên khoa
            sql = """
                SELECT * FROM Doctors 
                WHERE DoctorName LIKE %s OR Specialty LIKE %s 
                ORDER BY DoctorName
            """
            cursor.execute(sql, (search_term, search_term))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []
