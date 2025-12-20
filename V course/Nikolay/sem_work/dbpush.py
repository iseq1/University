import sqlite3
import hashlib

class DataPusher:
    def __init__(self, db_name):
        self.db_name = db_name
        self.table_fields = {
            'content': ['idblock', 'short_title', 'imgs', 'altimg', 'title', 'contenttext', 'author', 'timestampdata'],
            'menu': ['id', 'type', 'name', 'price', 'description', 'photo_path'],
            'menu_description_info': ['id', 'menu_id', 'ingredient'],
            'menu_size_info': ['id', 'menu_id', 'size', 'kcal', 'protein', 'fat', 'carbohydrate'],
            'User': ['id', 'login', 'fullname', 'email', 'number', 'user_photo', 'rang', 'order_count', 'comment_count', 'average_points', 'like_count', 'dislike_count'],
            'barista': ['id', 'barista_login', 'name', 'work_time'],
            'admin': ['id', 'admin_login', 'name'],
            'schedule': ['id', 'barista_id', 'date', 'start_time', 'finish_time', 'work_time'],
            'users': ['id', 'username', 'password', 'role']
        }

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()


    def update_data(self, table, ID, **kwargs):
        try:
            if table in self.table_fields:
                fields = self.table_fields[table]
                query = f"UPDATE {table} SET"
                set_values = []
                params = []

                for field in fields:
                    if field in kwargs:
                        set_values.append(f" {field} = ?")
                        params.append(kwargs[field])

                if set_values:
                    query += ",".join(set_values)
                    query += f" WHERE ID = ?;"
                    params.append(ID)

                    self.cursor.execute(query, params)
                    print(f"Данные под ID - {ID} в таблице {table} были успешно обновлены")
                else:
                    print("Передайте хотя бы один аргумент для обновления данных")
            else:
                print(f"Таблицы {table} нет в списке доступных таблиц.")
        except Exception as e:
            print("Ошибка при обновлении данных:", e)

    def delete_data(self, table, ID):
        try:
            query = f"DELETE FROM {table} WHERE ID = ?"
            self.cursor.execute(query, (ID,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"Данные под ID {ID} из таблицы '{table}' успешно удалены")
            else:
                print(f"Запись с ID {ID} в таблице '{table}' не существует")
        except Exception as e:
            print("Ошибка удаления данных:", e)


    def insert_data(self, table, **kwargs):
        try:
            if table in self.table_fields:
                fields = self.table_fields[table][1:]  # Исключаем ID
                query = f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join(['?'] * len(fields))});"
                params = [kwargs[field] for field in fields]
                print(query, params)
                self.cursor.execute(query, params)
                self.conn.commit()

                print(f"Данные успешно добавлены в таблицу '{table}'")
            else:
                print(f"Таблицы {table} нет в списке доступных таблиц.")
        except Exception as e:
            print("Ошибка при добавлении данных:", e)

    def select_data(self, table, *fields, **conditions):
        try:
            if table in self.table_fields:
                if not fields:  # Если поля для выборки не указаны, выбираем все поля
                    fields = self.table_fields[table]  # Исключаем ID

                query = f"SELECT {','.join(fields)} FROM {table}"
                if conditions:
                    query += " WHERE " + " AND ".join([f"{key} = ?" for key in conditions.keys()])
                    params = list(conditions.values())
                else:
                    params = []
                self.cursor.execute(query, params)
                result = self.cursor.fetchall()
                return result
            else:
                print(f"Таблицы {table} нет в списке доступных таблиц.")
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)


    def create_smth(self, lst):
        # Подключение к нашей базе данных
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        values = []

        for item in lst:
            values.append([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]])

        c.executemany('INSERT INTO content (idblock, short_title, imgs, altimg, title, contenttext,  author, timestampdata) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values)
        # Сохранение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()



