from app.db.connection import get_db_connection
import mysql.connector

def get_all_treatments():
    """
    Lấy danh sách tất cả các loại điều trị.
    Sắp xếp theo tên (A-Z) để dễ tìm.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Treatments ORDER BY TreatmentName ASC")
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []

def get_treatment_by_id(treatment_id):
    """
    Lấy chi tiết 1 loại điều trị.
    Dùng cho form Sửa (Edit).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Treatments WHERE TreatmentID = %s", (treatment_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return None

def create_treatment(name, cost):
    """
    Thêm mới một loại điều trị.
    Tham số 'cost' (StandardCost) phải là số.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Treatments (TreatmentName, StandardCost) VALUES (%s, %s)"
            cursor.execute(sql, (name, cost))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return False

def update_treatment(treatment_id, name, cost):
    """
    Cập nhật tên và giá tiền chuẩn của điều trị.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE Treatments SET TreatmentName = %s, StandardCost = %s WHERE TreatmentID = %s"
            cursor.execute(sql, (name, cost, treatment_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return False

def delete_treatment(treatment_id):
    """
    Xóa loại điều trị.
    Lưu ý: Nếu loại điều trị này đã được sử dụng trong các Phiên điều trị (Sessions),
    việc xóa sẽ bị chặn bởi ràng buộc Khóa ngoại (Foreign Key) để bảo toàn dữ liệu lịch sử/tài chính.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Treatments WHERE TreatmentID = %s", (treatment_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Lỗi khi xóa điều trị: {err}")
            return False
    return False

def search_treatments(keyword):
    """
    Tìm kiếm điều trị theo Tên.
    Đáp ứng yêu cầu tìm kiếm toàn cục [2.4 Global Search].
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            search_term = f"%{keyword}%"
            sql = "SELECT * FROM Treatments WHERE TreatmentName LIKE %s ORDER BY TreatmentName"
            cursor.execute(sql, (search_term,))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []
