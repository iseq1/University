import socket
import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import scrolledtext, messagebox

from RSA import RSA
from Diffie_Hellman import DiffieHellman
from user_database import UserDatabase
from RC4 import RC4
from helper import generate_sw, hash_md5


class OriginalClient:
    def __init__(self, root, host='localhost', port=5000,):
        self.root = root
        self.root.title("Основной Клиент")
        self.host = host
        self.port = port
        self.db = UserDatabase()
        self.client_wait_form()
        self.conn = None
        self.rc4 = None
        self.rsa = None
        self.companion_e, self.companion_n = None, None

    def client_wait_form(self):
        self.label_login = tk.Label(root, text="Ожидание пользователя...")
        self.label_login.grid(row=1, column=1, padx=10, pady=10)

    def build_chat_interface(self):
        self.clear_page()
        # Текстовое поле для чата с прокруткой (большое поле для отображения сообщений)
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='normal', height=20, width=80)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.chat_display.tag_configure("name_C", foreground="#3CB371", font=("Arial", 10, "italic", "bold"))
        self.chat_display.tag_configure("post_message_C", foreground="#FFA07A")
        self.chat_display.tag_configure("name_OC", foreground="#4682B4", font=("Arial", 10, "italic", "bold"))
        self.chat_display.tag_configure("post_message_OC", foreground="#FFA07A")

        # Поле ввода для сообщений
        self.message_entry = tk.Entry(self.root, width=60)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        # Кнопка "Отправить" для текущего ввода сообщения
        self.send_button = tk.Button(self.root, text="Отправить", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        self.generate_key_button = tk.Button(self.root, text="Сгенерировать", command=self.generate_keys)
        self.generate_key_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.send_keys_button = tk.Button(self.root, text="Отправить", command=self.send_keys, state="disabled")
        self.send_keys_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Настройка для растягивания виджетов по горизонтали и вертикали
        self.root.grid_rowconfigure(0, weight=1)  # Растягивание текстового поля
        self.root.grid_columnconfigure(0, weight=1)  # Растягивание первой колонки
        self.root.grid_columnconfigure(1, weight=0)  # Вторая колонка фиксированной ширины

    def go_to_chat(self, conn):
        self.conn = conn
        self.trade_keys(conn)  # Обмен ключами
        self.conn.settimeout(None)

        self.build_chat_interface()

        # Запускаем поток для приема сообщений
        receive_thread = threading.Thread(target=self.receive_message, daemon=True)
        receive_thread.start()

    def trade_keys(self, conn):
        conn.settimeout(10.0)

        data = conn.recv(4096).decode()
        # Получаем A, g, p от основного клиента
        A, g, p = map(int, data.split('|'))

        print(f"Получены данные от основного клиента:")
        print(f"A: {A}")
        print(f"g: {g}")
        print(f"p: {p}")

        diffie_hellman = DiffieHellman(g=g, p=p)
        # b - 64-битное нечетное число
        print(f"Сгенерировано число b: {diffie_hellman.b}")

        # Вычисляем B = g^b mod p
        B = diffie_hellman.make_B()
        print(f"Вычислено B: {B}")

        conn.send(str(B).encode())
        print(f"Отправлено B: {B}")

        # Вычисляем сеансовый ключ K = A^b mod p
        K = diffie_hellman.make_K(A, diffie_hellman.b, p)
        print(f"Вычислен сеансовый ключ K: {K}")
        self.rc4 = RC4(str(K))

    def generate_keys(self):
        self.rsa = RSA()
        print(f"Сгенерированы ключи RSA: e={self.rsa.e}, n={self.rsa.n}, d={self.rsa.d}")
        self.send_keys_button.config(state="normal")

    def send_keys(self):
        """Отправка открытого ключа клиенту."""
        if self.rsa.e is not None and self.rsa.n is not None:
            public_key = f"RSA-KEYS|{self.rsa.e}|{self.rsa.n}"
            encrypted_key = self.rc4.encrypt(public_key)
            if self.conn:
                try:
                    self.conn.send((encrypted_key + "\n").encode())
                    print(f"Отправлен открытый ключ: e={self.rsa.e}, n={self.rsa.n}")
                except Exception as e:
                    print(f"Ошибка отправки ключа: {e}")
                    self.conn.close()

    def send_message(self):
        message = self.message_entry.get()
        if message and message!="":
            try:
                # Шифруем сообщение с использованием RC4 и ключа K
                encrypted_message = self.rc4.encrypt(message)

                # Отправляем зашифрованное сообщение другому клиенту через соединение (conn)
                self.conn.send(encrypted_message.encode())

                # Отображаем отправленное зашифрованное сообщение в чате
                premessage = '📍'
                name = f"Основной клиент: "
                postmessage = f" ({encrypted_message})\n"

                self.chat_display.insert(tk.END, premessage)
                self.chat_display.insert(tk.END, name, "name_OC")
                self.chat_display.insert(tk.END, message)
                self.chat_display.insert(tk.END, postmessage, "post_message_OC")


                # Очищаем поле ввода
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
                self.conn.close()  # Закрыть сокет при ошибке
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите сообщение")

    def receive_message(self):
        try:
            # print(f"Receiving messages from: {self.conn}")
            while True:
                if not self.conn.fileno() == -1:  # Проверка, что сокет все еще активен
                    encrypted_message = self.conn.recv(1024).decode()
                    if not encrypted_message:
                        break

                    decrypted_message = self.rc4.decrypt(encrypted_message)

                    if str(decrypted_message).startswith("RSA-KEYS"):
                        tag, self.companion_e, self.companion_n = str(decrypted_message).split('|')
                        print(f'Получен открытый ключ Client: e={self.companion_e}, n={self.companion_n}')
                    elif str(decrypted_message).startswith("ECP|"):
                        tag, file_data, signature = str(decrypted_message).split('|')
                        self.verify_signature(file_data=file_data, signature=signature)
                    else:
                        premessage = '💬'
                        name = f"Клиент: "
                        postmessage = f" ({encrypted_message})\n"

                        self.chat_display.insert(tk.END, premessage)
                        self.chat_display.insert(tk.END, name, "name_C")
                        self.chat_display.insert(tk.END, decrypted_message)
                        self.chat_display.insert(tk.END, postmessage, "post_message_C")

                else:
                    print('Сокет неактивен')
                    break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")

    def verify_signature(self, file_data, signature):
        print(f"Полученный файл: {file_data}")
        print(f"Полученный X: {signature}")
        # H` - хеш файла
        file_hash = hash_md5(file_data)
        print(f"Хеш файла: {file_hash}")

        import re

        cleaned_signature = re.sub(r'\D', '', signature)

        # Z = X^e mod n
        calculated_hash = self.rsa.mod_exp(int(re.sub(r'\D', '', signature)), int(re.sub(r'\D', '', self.companion_e)), int(re.sub(r'\D', '', self.companion_n)))
        print(f"Вычисленная (Z): {calculated_hash}")

        if int(file_hash, 16) == calculated_hash:
            messagebox.showinfo('Подпись верна', 'Подпись файла верна.')
            print(f"H`: {int(file_hash, 16)}")
            print(f"Вычисленная (Z): {calculated_hash}")
            print("Подпись файла верна.")
        else:
            messagebox.showerror('Подпись неверна', 'Подпись файла неверна.')
            print("Подпись файла неверна.")
            print(f"Полученная подпись: {signature}")
            print(f"Вычисленная подпись (Z): {calculated_hash}")

    def clear_page(self):
        # Удаляем все элементы интерфейса
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_server(self):
        """Запуск сервера для прослушивания подключений."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Сервер запущен на {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Подключение от: {addr}")
            client_thread = threading.Thread(target=self.user_authentication, args=(client_socket,))
            client_thread.start()

    def user_authentication(self, conn):
        """Обработка аутентификации методом слова-вызова."""
        try:
            login = conn.recv(1024).decode('utf-8')
            print(f"Аутентификация пользователя: {login}")

            # Проверка логина в базе данных
            success, message, data = self.db.get_user(login)
            if not success:
                print("Пользователь не найден. Отправка NOT_FOUND...")
                conn.send("NOT_FOUND")
                # self.close()
                # self.close_window_signal.emit()
                print("Соединение закрыто.")
                # conn.send("Логин не найден".encode('utf-8'))
                return False


            # Генерация слова-вызова (128-битная строка)
            sw = generate_sw()
            sw_time = datetime.now() + timedelta(hours=24)
            print(f"SW: {sw}, Time: {sw_time}")

            self.db.update_user_auth(login, sw, sw_time)

            # Хэшируем слово-вызов
            sw_hash = hash_md5(sw)
            print(f"Сгенерированный хеш sw: {sw_hash}")
            conn.send(sw_hash.encode('utf-8'))

            # Получаем хэш S от клиента
            s_hash = conn.recv(1024).decode('utf-8')
            print(f"Полученный хеш s от клиента: {s_hash}")

            # Проверка срока действия слова-вызова
            stored_password = data[1]
            print('stored_password:', stored_password)
            server_hash = hash_md5(hash_md5(sw) + stored_password)
            print(f"Хеш s` на основном клиенте: {server_hash}")

            # Проверка s` = s
            if s_hash != server_hash:
                print("Неверный пароль. Отправка WRONG_PASSWORD...")
                conn.send("WRONG_PASSWORD".encode('utf-8'))
                # self.close()
                # self.close_window_signal.emit()
                print("Соединение закрыто.")
                return False

            print("Аутентификация прошла успешно. Отправка SUCCESS...")
            conn.send("SUCCESS".encode('utf-8'))
            self.go_to_chat(conn)



        except Exception as e:
            print(f"Ошибка: {e}")
        # finally:
        #     conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    client1 = OriginalClient(root)
    threading.Thread(target=client1.start_server, daemon=True).start()

    root.mainloop()
