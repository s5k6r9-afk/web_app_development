from . import get_db_connection
from datetime import date

class Record:
    @staticmethod
    def create(user_id, card_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        today = date.today().isoformat()
        cursor.execute(
            'INSERT INTO records (user_id, card_id, date) VALUES (?, ?, ?)',
            (user_id, card_id, today)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        # 可以結合 JOIN 來獲取更完整的資訊 (包含了卡片名稱等等)
        query = '''
            SELECT r.*, c.name, c.theme, c.description, c.image_url 
            FROM records r
            JOIN cards c ON r.card_id = c.id
            WHERE r.id = ?
        '''
        record = conn.execute(query, (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def get_all(user_id=None):
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
        conn.close()
        return [dict(r) for r in records]

    @staticmethod
    def has_drawn_today(user_id):
        conn = get_db_connection()
        today = date.today().isoformat()
        record = conn.execute(
            'SELECT * FROM records WHERE user_id = ? AND date = ?',
            (user_id, today)
        ).fetchone()
        conn.close()
        return record is not None

    @staticmethod
    def update(record_id, card_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE records SET card_id = ? WHERE id = ?', (card_id, record_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
