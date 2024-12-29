import sqlite3
import os
from helper import hash_md5


class UserDatabase:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Создание таблицы пользователей, если её ещё нет."""
        if not os.path.exists(self.db_path):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        login TEXT PRIMARY KEY,
                        password_hash TEXT,
                        sw TEXT,
                        t TEXT
                    )
                """)
                conn.commit()

    def get_user(self, login):
        """Изъятие юзера из бд"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
                user = cursor.fetchone()
                conn.commit()

            if user:  # Проверяем, существует ли пользователь
                return True, "Пользователь успешно найден", user
            else:
                return False, "Пользователя с таким логином не существует"
        except sqlite3.IntegrityError:
            return False, "Ошибка доступа к базе данных"

    @staticmethod
    def hash_password(password):
        """Хэширование пароля с использованием MD5."""
        return hash_md5(password)

    def register_user(self, login, password):
        """Регистрация пользователя в базе данных."""
        password_hash = self.hash_password(password)
        sw = t = ""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (login, password_hash, sw, t) VALUES (?, ?, ?, ?)", (login, password_hash, sw, t))
                conn.commit()
            return True, "Пользователь зарегистрирован успешно"
        except sqlite3.IntegrityError:
            return False, "Пользователь с таким логином уже существует"

    def update_user_auth(self, login, sw, sw_time):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET sw = ?, t = ? WHERE login = ?", (sw, sw_time, login))
                conn.commit()
            return True, "Данные пользователя успешно обновлены"
        except sqlite3.IntegrityError:
            return False, "Ошибка при обновлении токена"
