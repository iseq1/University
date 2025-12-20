import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS User (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             login TEXT,
             fullname TEXT,
             email TEXT,
             number TEXT,
             rang TEXT,
             order_count INTEGER,
             average_points REAL
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT,
             role TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS menu (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             type TEXT,
             name TEXT,
             price REAL,
             description TEXT,
             photo_path TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS menu_description_info (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             menu_id TEXT,
             ingredient TEXT,
             FOREIGN KEY(menu_id) REFERENCES menu(id)
             )''')

c.execute('''
    CREATE TABLE IF NOT EXISTS menu_size_info (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         menu_id TEXT,
         size TEXT,
         kcal REAL,
         protein REAL,
         fat REAL,
         carbohydrate REAL,
         FOREIGN KEY(menu_id) REFERENCES menu(id)
     )''')



c.execute('''
    CREATE TABLE IF NOT EXISTS personal_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            size TEXT NOT NULL,
            menu_id INTEGER NOT NULL,
            FOREIGN KEY(menu_id) REFERENCES menu(id)
    )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS orders_has_order (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        orders_id INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES personal_order(id),
        FOREIGN KEY(orders_id) REFERENCES orders(id)
    )
    ''')



c.execute('''
       CREATE TABLE IF NOT EXISTS orders (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           order_date TEXT NOT NULL,
           stars INTEGER NOT NULL,
           barista_id INTEGER NOT NULL,
           User_id INTEGER NOT NULL,
           FOREIGN KEY(barista_id) REFERENCES barista(id),
           FOREIGN KEY(User_id) REFERENCES User(id)
       )
   ''')



c.execute('''
       CREATE TABLE IF NOT EXISTS barista (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           barista_login TEXT NOT NULL,
           name TEXT NOT NULL,
           work_time INTEGER NOT NULL,
           FOREIGN KEY(barista_login) REFERENCES users(username)
       )
    ''')

c.execute('''
    CREATE TABLE IF NOT EXISTS admin (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       admin_login TEXT NOT NULL,
       name TEXT NOT NULL,
       FOREIGN KEY(admin_login) REFERENCES users(username)
    )
    ''')


c.execute('''
       CREATE TABLE IF NOT EXISTS schedule (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
            barista_id INTEGER NOT NULL,
           date TEXT NOT NULL,
           start_time TEXT NOT NULL,
            finish_time TEXT NOT NULL,
           work_time INTEGER NOT NULL,
           FOREIGN KEY(barista_id) REFERENCES barista(id)
       )
    ''')

# Закрытие соединения с базой данных
conn.close()
