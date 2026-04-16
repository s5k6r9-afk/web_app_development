import sqlite3
from . import get_db_connection

class User:
    """處理 Users 資料表的資料操作邏輯"""

    @staticmethod
    def create(username, email, password_hash):
        """
        新增一位使用者紀錄。
        :param username: (str) 使用者名稱
        :param email: (str) 電子郵件
        :param password_hash: (str) 雜湊後的密碼
        :return: (int) 新紀錄的 ID，若失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"[User.create] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        透過 ID 取得單筆使用者。
        :param user_id: (int) 使用者 ID
        :return: (dict) 使用者資料，若無資料則為 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"[User.get_by_id] 資料庫操作發生錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_email(email):
        """
        透過 Email 取得使用者，常應用於登入驗證。
        :param email: (str) 電子郵件
        :return: (dict) 使用者資料，若無資料則為 None
        """
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"[User.get_by_email] 資料庫操作發生錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者紀錄。
        :return: (list of dict) 使用者資料列表
        """
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            return [dict(u) for u in users]
        except sqlite3.Error as e:
            print(f"[User.get_all] 資料庫操作發生錯誤: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(user_id, username=None, email=None, password_hash=None):
        """
        更新指定的會員資料。
        :param user_id: (int) 欲更新的使用者 ID
        :param username: (str) 新名稱 (選填)
        :param email: (str) 新郵件 (選填)
        :param password_hash: (str) 新密碼 (選填)
        :return: (bool) 是否更新成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            if username:
                updates.append('username = ?')
                params.append(username)
            if email:
                updates.append('email = ?')
                params.append(email)
            if password_hash:
                updates.append('password_hash = ?')
                params.append(password_hash)
                
            if not updates:
                return True

            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, tuple(params))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[User.update] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除使用者紀錄。
        :param user_id: (int) 使用者 ID
        :return: (bool) 是否刪除成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[User.delete] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
