from app.db.connection import get_db_connection
import mysql.connector

def get_all_sessions():
    """
    Lấy danh sách phiên điều trị.
    QUAN TRỌNG: Sử dụng JOIN để lấy tên thay vì chỉ hiện ID.
    Dữ liệu trả về sẽ gồm: SessionID, Ngày, Tên BN, Tên BS, Tên Điều trị, Chi phí.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT 
                    s.SessionID, 
                    s.TreatmentDate, 
                    p.PatientName, 
                    d.DoctorName, 
                    t.TreatmentName,
                    t.StandardCost
                FROM TreatmentSessions s
                JOIN Patients p ON s.PatientID = p.PatientID
                JOIN Doctors d ON s.DoctorID = d.DoctorID
                JOIN Treatments t ON s.TreatmentID = t.TreatmentID
                ORDER BY s.TreatmentDate DESC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return []

def get_session_by_id(session_id):
    """
    Lấy chi tiết 1 phiên điều trị theo SessionID.
    Dùng cho chức năng Sửa (Edit).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM TreatmentSessions WHERE SessionID = %s"
            cursor.execute(sql, (session_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    return None

def create_session(patient_id, doctor_id, treatment_id, treatment_date):
    """
    Tạo phiên điều trị mới.
    Lưu ý: Các tham số đầu vào là ID (được chọn từ Dropdown trên giao diện).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO TreatmentSessions (PatientID, DoctorID, TreatmentID, TreatmentDate) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (patient_id, doctor_id, treatment_id, treatment_date))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating session: {err}")
    return False

def update_session(session_id, patient_id, doctor_id, treatment_id, treatment_date):
    """
    Cập nhật thông tin phiên điều trị.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """
                UPDATE TreatmentSessions 
                SET PatientID = %s, DoctorID = %s, TreatmentID = %s, TreatmentDate = %s 
                WHERE SessionID = %s
            """
            cursor.execute(sql, (patient_id, doctor_id, treatment_id, treatment_date, session_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error updating session: {err}")
    return False

def delete_session(session_id):
    """
    Xóa phiên điều trị.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM TreatmentSessions WHERE SessionID = %s", (session_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting session: {err}")
    return False

def search_sessions(keyword):
    """
    Tìm kiếm phiên điều trị.
    Tìm theo tên Bệnh nhân HOẶC tên Bác sĩ.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            search_term = f"%{keyword}%"
            sql = """
                SELECT 
                    s.SessionID, s.TreatmentDate, 
                    p.PatientName, d.DoctorName, t.TreatmentName, t.StandardCost
                FROM TreatmentSessions s
                JOIN Patients p ON s.PatientID = p.PatientID
                JOIN Doctors d ON s.DoctorID = d.DoctorID
                JOIN Treatments t ON s.TreatmentID = t.TreatmentID
                WHERE p.PatientName LIKE %s OR d.DoctorName LIKE %s
                ORDER BY s.TreatmentDate DESC
            """
            cursor.execute(sql, (search_term, search_term))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except mysql.connector.Error as err:
            print(f"Error searching sessions: {err}")
    return []
