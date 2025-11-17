from app.db.connection import get_db_connection
import mysql.connector

def get_all_patients():
    """
    Lấy danh sách tất cả bệnh nhân.
    Sắp xếp theo ID giảm dần (người mới nhất lên đầu).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True) 
            cursor.execute("SELECT * FROM Patients ORDER BY PatientID DESC")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []

def get_patient_by_id(patient_id):
    """
    Lấy thông tin chi tiết của 1 bệnh nhân cụ thể.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Dấu phẩy sau patient_id là bắt buộc để tạo tuple 1 phần tử
            cursor.execute("SELECT * FROM Patients WHERE PatientID = %s", (patient_id,))
            result = cursor.fetchone() # Chỉ lấy 1 dòng
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return None

def create_patient(name, birthdate):
    """
    Thêm mới một bệnh nhân.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Patients (PatientName, Birthdate) VALUES (%s, %s)"
            cursor.execute(sql, (name, birthdate))
            conn.commit() # Lưu thay đổi vào DB
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return False

def update_patient(patient_id, name, birthdate):
    """
    Cập nhật thông tin bệnh nhân.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE Patients SET PatientName = %s, Birthdate = %s WHERE PatientID = %s"
            cursor.execute(sql, (name, birthdate, patient_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return False

def delete_patient(patient_id):
    """
    Xóa bệnh nhân.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Patients WHERE PatientID = %s", (patient_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa: {err}")
            return False
    return False

def search_patients(keyword):
    """
    Tìm kiếm bệnh nhân theo tên (Global Search).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Thêm dấu % để tìm kiếm gần đúng (LIKE)
            search_term = f"%{keyword}%"
            sql = "SELECT * FROM Patients WHERE PatientName LIKE %s ORDER BY PatientName"
            cursor.execute(sql, (search_term,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []

