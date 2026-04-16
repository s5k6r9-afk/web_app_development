import sqlite3
from . import get_db_connection

class DivCard:
    """處理 cards 牌卡題庫表的資料操作邏輯"""

    @staticmethod
    def create(theme, name, description, image_url=None):
        """
        新增一張牌卡或籤詩。
        :param theme: (str) 牌卡所屬主題
        :param name: (str) 卡片名稱
        :param description: (str) 解說內容
        :param image_url: (str) 圖片路徑 (選填)
        :return: (int) 新增後的卡片 ID，失敗為 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO cards (theme, name, description, image_url) VALUES (?, ?, ?, ?)',
                (theme, name, description, image_url)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"[DivCard.create] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_by_id(card_id):
        """
        透過 ID 獲取單張牌卡資料。
        :param card_id: (int) 牌卡 ID
        :return: (dict) 卡片資料
        """
        try:
            conn = get_db_connection()
            card = conn.execute('SELECT * FROM cards WHERE id = ?', (card_id,)).fetchone()
            return dict(card) if card else None
        except sqlite3.Error as e:
            print(f"[DivCard.get_by_id] 資料庫操作發生錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_all(theme=None):
        """
        獲取牌卡列表。
        :param theme: (str) 選填，若是提供則僅查詢該主題卡片
        :return: (list of dict) 卡片清單
        """
        try:
            conn = get_db_connection()
            if theme:
                cards = conn.execute('SELECT * FROM cards WHERE theme = ?', (theme,)).fetchall()
            else:
                cards = conn.execute('SELECT * FROM cards').fetchall()
            return [dict(c) for c in cards]
        except sqlite3.Error as e:
            print(f"[DivCard.get_all] 資料庫操作發生錯誤: {e}")
            return []
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def get_random_by_theme(theme):
        """
        隨機從指定主題中抽出一張卡片。
        :param theme: (str) 給定抽卡分類
        :return: (dict) 單張牌卡，若題庫為空則回傳 None
        """
        try:
            conn = get_db_connection()
            card = conn.execute('SELECT * FROM cards WHERE theme = ? ORDER BY RANDOM() LIMIT 1', (theme,)).fetchone()
            return dict(card) if card else None
        except sqlite3.Error as e:
            print(f"[DivCard.get_random_by_theme] 資料庫操作發生錯誤: {e}")
            return None
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def update(card_id, theme=None, name=None, description=None, image_url=None):
        """
        更新牌卡資訊。
        :param card_id: (int) 欲更新之卡片 ID
        :return: (bool) 成功與否
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            if theme:
                updates.append('theme = ?')
                params.append(theme)
            if name:
                updates.append('name = ?')
                params.append(name)
            if description:
                updates.append('description = ?')
                params.append(description)
            if image_url is not None:
                updates.append('image_url = ?')
                params.append(image_url)
                
            if not updates:
                return True
                
            params.append(card_id)
            query = f"UPDATE cards SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, tuple(params))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DivCard.update] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()

    @staticmethod
    def delete(card_id):
        """
        刪除特定牌卡。
        :param card_id: (int) ID
        :return: (bool) 成功與否
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DivCard.delete] 資料庫操作發生錯誤: {e}")
            if 'conn' in locals() and conn: conn.rollback()
            return False
        finally:
            if 'conn' in locals() and conn: conn.close()
