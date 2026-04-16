from . import get_db_connection

class DivCard:
    @staticmethod
    def create(theme, name, description, image_url=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO cards (theme, name, description, image_url) VALUES (?, ?, ?, ?)',
            (theme, name, description, image_url)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_id(card_id):
        conn = get_db_connection()
        card = conn.execute('SELECT * FROM cards WHERE id = ?', (card_id,)).fetchone()
        conn.close()
        return dict(card) if card else None

    @staticmethod
    def get_all(theme=None):
        conn = get_db_connection()
        if theme:
            cards = conn.execute('SELECT * FROM cards WHERE theme = ?', (theme,)).fetchall()
        else:
            cards = conn.execute('SELECT * FROM cards').fetchall()
        conn.close()
        return [dict(c) for c in cards]

    @staticmethod
    def get_random_by_theme(theme):
        conn = get_db_connection()
        # 利用 SQLite 內建的 ORDER BY RANDOM() 隨機取得一張
        card = conn.execute('SELECT * FROM cards WHERE theme = ? ORDER BY RANDOM() LIMIT 1', (theme,)).fetchone()
        conn.close()
        return dict(card) if card else None

    @staticmethod
    def update(card_id, theme=None, name=None, description=None, image_url=None):
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
            conn.close()
            return
            
        params.append(card_id)
        query = f"UPDATE cards SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, tuple(params))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(card_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
        conn.commit()
        conn.close()
