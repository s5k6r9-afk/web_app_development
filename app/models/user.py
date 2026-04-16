from . import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def update(user_id, username=None, email=None, password_hash=None):
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
            conn.close()
            return

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, tuple(params))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
