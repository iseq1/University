import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from helper import hash_md5
import threading
import re
from user_database import UserDatabase
from Diffie_Hellman import DiffieHellman
from RC4 import RC4
from RSA import RSA


class ClientApp:
    def __init__(self, root):
        self.db = UserDatabase()
        self.root = root
        self.conn = None
        self.root.title("Клиент")
        self.show_registration_page()
        self.rc4 = None
        self.rsa = None
        self.companion_e, self.companion_n = None, None
        self.file_path = None

    def show_registration_page(self):
        self.clear_page()
        root = self.root

        self.main_label = tk.Label(root, text="Регистрация")
        self.main_label.grid(row=0, column=1, padx=10, pady=10)

        self.label_login = tk.Label(root, text="Логин:")
        self.label_login.grid(row=1, column=0, padx=10, pady=10)

        self.entry_login = tk.Entry(root)
        self.entry_login.grid(row=1, column=1, padx=10, pady=10)

        self.label_password = tk.Label(root, text="Пароль:")
        self.label_password.grid(row=2, column=0, padx=10, pady=10)

        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        self.register_button = tk.Button(root, text="Зарегистрироваться", command=self.register_user)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.login_button = tk.Button(root, text="Уже есть аккаунт", command=self.show_login_page)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20)

    def show_login_page(self):
        self.clear_page()
        # Элементы интерфейса

        self.main_label = tk.Label(root, text="Авторизация")
        self.main_label.grid(row=0, column=1, padx=10, pady=10)

        self.label_login = tk.Label(root, text="Логин:")
        self.label_login.grid(row=1, column=0, padx=10, pady=10)

        self.entry_login = tk.Entry(root)
        self.entry_login.grid(row=1, column=1, padx=10, pady=10)

        self.label_password = tk.Label(root, text="Пароль:")
        self.label_password.grid(row=2, column=0, padx=10, pady=10)

        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        self.login_button = tk.Button(root, text="Авторизоваться", command=self.authenticate_user)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.register_button = tk.Button(root, text="Ещё нет аккаунта", command=self.show_registration_page)
        self.register_button.grid(row=4, column=0, columnspan=2, pady=20)

    def validate_input(self, login, password):
        """Валидация логина и пароля."""
        if not re.match(r"^\w{4,20}$", login):
            return False, "Логин должен содержать от 4 до 20 символов и состоять только из букв, цифр и символа подчёркивания."

        if len(password) < 8:
            return False, "Пароль должен содержать как минимум 8 символов."

        if not any(char.isdigit() for char in password):
            return False, "Пароль должен содержать хотя бы одну цифру."

        if not any(char.isalpha() for char in password):
            return False, "Пароль должен содержать хотя бы одну букву."

        if password == password.lower() or password == password.upper():
            return False, "Пароль должен содержать символы разных регистров."

        if " " in login or " " in password:
            return False, "Логин и пароль не должны содержать пробелы."

        return True, ""

    def register_user(self):
        """Регистрация пользователя через UserDatabase."""
        login = self.entry_login.get()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Валидация данных
        is_valid, message = self.validate_input(login, password)
        if not is_valid:
            messagebox.showerror("Ошибка", message)
            return

        success, message = self.db.register_user(login, password)

        if success:
            messagebox.showinfo("Успех", message)
            self.entry_login.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", message)

    def authenticate_user(self):
        """Отправка логина для аутентификации."""
        login = self.entry_login.get()
        password = self.entry_password.get()
        if not login or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:

            # Подключение к Original Client (Client 1)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            user = self.db.get_user(login=login)
            if not user[0]:
                raise Exception("Пользователя с таким логином не существует")
            else:
                client_socket.connect(('localhost', 5000))
                # Отправляем логин
                client_socket.send(login.encode('utf-8'))

                # Получаем слово-вызов (SW) от сервера
                response = client_socket.recv(1024).decode('utf-8')

                if response == "NOT_FOUND":
                    messagebox.showerror("Ошибка", "Логин не найден")
                    return

                print(f"Захешированный sw от основного клиента: {response}")
                # Хэшируем пароль
                password_hash = hash_md5(password)
                print("Хэшированный пароль: ", password_hash)

                # Конкатенируем хэш пароля и слово-вызов
                # s_hash = хеш(хеш SW + хеш пароля)
                s_hash = hash_md5(response + password_hash)
                print(f"Суперхеш: {s_hash}")

                # Отправляем хэш S серверу
                client_socket.send(s_hash.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                if response == "WRONG_PASSWORD":
                    messagebox.showerror("Ошибка", "Неверно указан пароль")
                    return
                elif response == "SUCCESS":
                    # messagebox.showinfo("Успех", "Хэш отправлен серверу для проверки")
                    self.go_to_chat(conn=client_socket)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при подключении: {e}")
        # finally:
        #     client_socket.close()

    def clear_page(self):
        # Удаляем все элементы интерфейса
        for widget in self.root.winfo_children():
            widget.destroy()

    def go_to_chat(self, conn):
        self.conn = conn
        self.trade_keys(conn)
        self.conn.settimeout(None)
        self.build_chat_interface()
        # Запускаем поток для приема сообщений
        receive_thread = threading.Thread(target=self.receive_message, daemon=True)
        receive_thread.start()

    def build_chat_interface(self):
        self.clear_page()
        # Текстовое поле для чата с прокруткой (большое поле для отображения сообщений)
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='normal', height=20, width=80)
        self.chat_display.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.chat_display.tag_configure("name_OC", foreground="#3CB371", font=("Arial", 10, "italic", "bold"))
        self.chat_display.tag_configure("post_message_OC", foreground="#FFA07A")
        self.chat_display.tag_configure("name_C", foreground="#4682B4", font=("Arial", 10, "italic", "bold"))
        self.chat_display.tag_configure("post_message_C", foreground="#FFA07A")
        # Поле ввода для сообщений
        self.message_entry = tk.Entry(self.root, width=60)
        self.message_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Кнопка "Отправить" для текущего ввода сообщения
        self.send_button = tk.Button(self.root, text="Отправить", command=self.send_message)
        self.send_button.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        # Две кнопки для следующих этапов: "Сгенерировать" и "Отправить"
        self.generate_button = tk.Button(self.root, text="Сгенерировать", command=self.generate_keys)
        self.generate_button.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        self.next_send_button = tk.Button(self.root, text="Отправить", command=self.send_keys, state="disabled")
        self.next_send_button.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        # Две дополнительные кнопки: "Загрузить файл" и "Подписать и отправить"
        self.upload_file_button = tk.Button(self.root, text="Загрузить файл", command=self.upload_file, state="disabled")
        self.upload_file_button.grid(row=3, column=0, padx=10, pady=5, sticky="we")

        self.sign_and_send_button = tk.Button(self.root, text="Подписать и отправить", command=self.sign_and_send, state="disabled")
        self.sign_and_send_button.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        # Настройка для растягивания виджетов по горизонтали и вертикали
        self.root.grid_rowconfigure(0, weight=1)  # Растягивание текстового поля
        self.root.grid_columnconfigure(0, weight=1)  # Растягивание первой колонки
        self.root.grid_columnconfigure(1, weight=1)  # Растягивание второй колонки
        self.root.grid_columnconfigure(2, weight=0)  # Третья колонка для кнопки "Отправить"

    def trade_keys(self, conn):
        try:
            diffie_hellman = DiffieHellman()
            A = diffie_hellman.make_A()

            print(f"Сгенерировано число a: {diffie_hellman.a}")
            print(f"Генератор g: {diffie_hellman.g}")
            print(f"Сгенерировано простое число p: {diffie_hellman.p}")
            print(f"Вычислено число A: {A}")

            # Установим таймаут
            conn.settimeout(5.0)

            conn.send(f"{A}|{diffie_hellman.g}|{diffie_hellman.p}".encode())
            print("A, g, p отправлены клиенту")
            B = int(conn.recv(4096).decode())
            print(f"Получено число B от клиента: {B}")

            # Вычисление K = B^a mod p
            K = diffie_hellman.make_K(B, diffie_hellman.a, diffie_hellman.p)
            print(f"Вычислен сеансовый ключ K: {K}")
            self.rc4 = RC4(str(K))
        except Exception as e:
            print(f"Ошибка при обмене ключами: {e}")
            return False

    def generate_keys(self):
        self.rsa = RSA()
        print(f"Сгенерированы ключи RSA: e={self.rsa.e}, n={self.rsa.n}, d={self.rsa.d}")
        self.next_send_button.config(state="normal")

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
        self.check_both_key()


    def send_message(self):
        message = self.message_entry.get()
        if message and message!="":
            try:
                # Шифруем сообщение с использованием RC4 и ключа K
                encrypted_message = self.rc4.encrypt(message)

                # Отправляем зашифрованное сообщение другому клиенту через соединение (conn)
                self.conn.send(encrypted_message.encode())

                # Отображаем отправленное зашифрованное сообщение в чате
                premessage = '💬'
                name = f"Клиент: "
                postmessage = f" ({encrypted_message})\n"



                self.chat_display.insert(tk.END, premessage)
                self.chat_display.insert(tk.END, name, "name_C")
                self.chat_display.insert(tk.END, message)
                self.chat_display.insert(tk.END, postmessage, "post_message_C")


                # Очищаем поле ввода
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")
                self.conn.close()  # Закрыть сокет при ошибке
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите сообщение")

    def check_both_key(self):
        if self.rsa is not None and self.companion_n is not None and self.companion_n is not None:
            self.upload_file_button.config(state="normal")

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
                        print(f'Получен открытый ключ OGClient: e={self.companion_e}, n={self.companion_n}')
                        self.check_both_key()
                    else:

                        premessage = '📍'
                        name = f"Основной клиент: "
                        postmessage = f" ({encrypted_message})\n"

                        self.chat_display.insert(tk.END, premessage)
                        self.chat_display.insert(tk.END, name, "name_OC")
                        self.chat_display.insert(tk.END, decrypted_message)
                        self.chat_display.insert(tk.END, postmessage, "post_message_OC")

                else:
                    break
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")

    def upload_file(self):
        # Открываем диалоговое окно для выбора файла
        file_path = filedialog.askopenfilename(
            title="Выберите .txt файл",
            filetypes=[("Text files", "*.txt")]
        )

        if file_path:
            try:
                # Считываем содержимое файла
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Проверяем количество символов
                if len(content) > 1000:
                    messagebox.showerror("Ошибка", "Файл превышает лимит в 1000 символов.")
                    return  # Прерываем выполнение функции

                self.file_path = file_path
                # Выводим путь и содержимое файла
                print(f"Файл успешно загружен: {file_path}")

                # Сообщаем об успешной загрузке
                messagebox.showinfo("Файл загружен", f"Файл успешно загружен!")
                self.sign_and_send_button.config(state="normal")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {e}")
                print(f"Ошибка при чтении файла: {e}")
                return

    def sign_and_send(self):
        if self.file_path is not None and self.rsa.d is not None and self.rsa.n is not None:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                file_data = file.read()
            file_data_hash = hash_md5(file_data)
            print(f"Хеш файла: {file_data_hash}")

            # X = H^d mod n
            signature = self.rsa.mod_exp(int(file_data_hash, 16), self.rsa.d, self.rsa.n)
            print(f"Файл подписан: {self.file_path}, X: {signature}")

            # Объединяем данные в одну строку
            command = f"ECP|{file_data}|{signature}"

            # Зашифровываем команду
            encrypted_command = self.rc4.encrypt(command)

            # Отправляем зашифрованную команду на основной клиент
            if self.conn:
                try:
                    self.conn.send((encrypted_command + "\n").encode())
                    print(f"Файл и подпись отправлены")
                except Exception as e:
                    print(f"Ошибка отправки файла и подписи: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
