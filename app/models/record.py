import sqlite3
from datetime import date
from . import get_db_connection

class Record:
    """處理 records 使用者占卜紀錄表的資料操作邏輯"""

    @staticmethod
    def create(user_id, card_id):
        """
        新增使用者的抽卡紀錄，會自動登記今天的日期。
        :param user_id: (int) 使用者 ID
        :param card_id: (int) 抽中的牌卡 ID
        :return: (int) 新增紀錄的 ID，若出錯則為 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            today = date.today().isoformat()
            cursor.execute(
                'INSERT INTO records (user_id, card_id, date) VALUES (?, ?, ?)',
                (user_id, card_id, today)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"[Record.create] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(record_id):
        """
        獲取特定單筆的占卜紀錄，包含該牌卡的詳細解說內容。
        :param record_id: (int) 欲查詢此紀錄的單號
        :return: (dict) 關聯合併後的紀錄與牌卡資料
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT r.*, c.name, c.theme, c.description, c.image_url 
                FROM records r
                JOIN cards c ON r.card_id = c.id
                WHERE r.id = ?
            '''
            record = conn.execute(query, (record_id,)).fetchone()
            return dict(record) if record else None
        except sqlite3.Error as e:
            print(f"[Record.get_by_id] 資料庫操作發生錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all(user_id=None):
        """
        獲取歷史紀錄總覽。
        :param user_id: (int) 選填，若有提供則僅查詢某使用者的紀錄
        :return: (list of dict) 關聯合併後的歷史陣列
        """
        try:
            conn = get_db_connection()
            if user_id:
                query = '''
                    SELECT r.*, c.name, c.theme, c.image_url 
                    FROM records r
                    JOIN cards c ON r.card_id = c.id
                    WHERE r.user_id = ?
                    ORDER BY r.created_at DESC
                '''
                records = conn.execute(query, (user_id,)).fetchall()
            else:
                records = conn.execute('SELECT * FROM records ORDER BY created_at DESC').fetchall()
            return [dict(r) for r in records]
        except sqlite3.Error as e:
            print(f"[Record.get_all] 資料庫操作發生錯誤: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def has_drawn_today(user_id):
        """
        確認傳入的該名會員，今日是否已經抽過牌（每日一抽檢核）。
        :param user_id: (int) 會員 ID
        :return: (bool) 是否抽過
        """
        try:
            conn = get_db_connection()
            today = date.today().isoformat()
            record = conn.execute(
                'SELECT * FROM records WHERE user_id = ? AND date = ?',
                (user_id, today)
            ).fetchone()
            return record is not None
        except sqlite3.Error as e:
            print(f"[Record.has_drawn_today] 資料庫操作發生錯誤: {e}")
            # 發生錯誤時預設阻擋抽卡或是根據情境作其他處理，此處保守回傳 True 以防異常
            return True
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(record_id, card_id):
        """
        更新歷史紀錄 (特殊管理需求才需要)。
        :param record_id: (int) 紀錄 ID
        :param card_id: (int) 要替換的卡片
        :return: (bool) 成功與否
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE records SET card_id = ? WHERE id = ?', (card_id, record_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Record.update] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(record_id):
        """
        刪除特定紀錄。
        :param record_id: (int)
        :return: (bool) 成功與否
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[Record.delete] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
