import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from Binary import BinaryCipher
# import sys
# print(hasattr(sys, 'set_int_max_str_digits'))  # Должно вернуть True


class TabButtons:
    def __init__(self, parent, content_frame):
        self.parent = parent
        self.content_frame = content_frame

        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.tabs = [
            {"name": "Вкладка 1", "button": None, "content": self.tab1_content},
            {"name": "Вкладка 2", "button": None, "content": self.tab2_content},
            {"name": "Вкладка 3", "button": None, "content": self.tab3_content},
        ]

        for idx, tab in enumerate(self.tabs):
            tab["button"] = tk.Button(
                self.button_frame, text=tab["name"],
                command=lambda idx=idx: self.show_content(idx)
            )
            tab["button"].pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.show_content(0)

    def show_content(self, tab_index):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.tabs[tab_index]["content"]()

    def validate_input(self, k):
        return k == 'k' or k.isdigit()

    def tab1_content(self):
        # Верхний фрейм с комбобоксами и полями ввода
        self.top_frame = tk.Frame(self.content_frame)
        self.top_frame.pack(pady=10)

        self.language_combo = ttk.Combobox(self.top_frame, values=["Русский", "Английский"])
        self.language_combo.pack(side=tk.LEFT, padx=5)
        self.language_combo.set("Выберите язык")

        self.binarization_button = tk.Button(self.top_frame, text="Почистить формочки", width=20,
                                             command=self.clean_tab_1)
        self.binarization_button.pack(pady=0)

        self.mid_framge = tk.Frame(self.content_frame)
        self.mid_framge.pack(pady=10)

        self.mid_frame_left = tk.Frame(self.mid_framge)
        self.mid_frame_left.pack(side=tk.LEFT, pady=10)

        self.mid_frame_right = tk.Frame(self.mid_framge)
        self.mid_frame_right.pack(side=tk.RIGHT, pady=10)


        # ScrolledText для ввода многострочного текста
        self.text_box_top_left = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_top_left.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_top_left.insert(tk.END, "Сюда введите сообщение")

        # ScrolledText для ввода многострочного текста
        self.text_box_top_right = scrolledtext.ScrolledText(self.mid_frame_right, height=3)
        self.text_box_top_right.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_top_right.insert(tk.END, "")

        # ScrolledText для ввода многострочного текста
        self.text_box_bot_left = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_bot_left.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_bot_left.insert(tk.END, "Сюда введите ключ")

        # ScrolledText для ввода многострочного текста
        self.text_box_bot_right = scrolledtext.ScrolledText(self.mid_frame_right, height=3)
        self.text_box_bot_right.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_bot_right.insert(tk.END, "")

        self.binarization_button = tk.Button(self.content_frame, text="Бинаризация", width=20,
                                       command=self.text_binarization)
        self.binarization_button.pack(pady=20)

        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        self.center_button_xor = tk.Button(self.content_frame, text="XOR", width=20,
                                       command=self.encrypt_xor_by_key)
        self.center_button_xor.pack(pady=20)

        self.mid_text_box = scrolledtext.ScrolledText(self.content_frame, height=3)
        self.mid_text_box.pack()
        self.mid_text_box.insert(tk.END, "")

        self.center_button_decrypt = tk.Button(self.content_frame, text="Расшифровать", width=20,
                                       command=self.decrypt_xor_by_key)
        self.center_button_decrypt.pack(pady=20)

        # Нижний фрейм с текстовыми полями и кнопками
        self.bottom_frame = tk.Frame(self.content_frame)
        self.bottom_frame.pack(pady=10)

        left_frame = tk.Frame(self.bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.left_text_box = scrolledtext.ScrolledText(left_frame, height=10, width=50)
        self.left_text_box.pack()
        self.left_text_box.insert(tk.END, "")


        right_frame = tk.Frame(self.bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        self.right_text_box = scrolledtext.ScrolledText(right_frame, height=10, width=50)
        self.right_text_box.pack()
        self.right_text_box.insert(tk.END, "")

    def text_binarization(self):
        try:
            language = self.language_combo.get()
            if language not in ['Русский', 'Английский']:
                raise Exception('Вы не выбрали язык!\nВыберите его!!!')

            self.left_text_box.delete("1.0", tk.END)
            self.right_text_box.delete("1.0", tk.END)
            self.mid_text_box.delete("1.0", tk.END)

            text = self.text_box_top_left.get("1.0", tk.END).strip()
            key = self.text_box_bot_left.get("1.0", tk.END).strip()
            print(BinaryCipher().clean_string(key).lower())
            if text in ['' or 'Сюда введите сообщение']:
                raise Exception('Вы не ввели текст!\nВведите его!!!')
            if key in ['' or 'Сюда введите ключ']:
                raise Exception('Вы не ввели ключ!\nВведите его!!!')
            if text != BinaryCipher().clean_string(text).lower() or key != BinaryCipher().clean_string(key).lower():
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            if not BinaryCipher().check_alphabeta(text, _lang='ru' if language=="Русский" else 'en'):
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")
            if BinaryCipher().check_key(text) or BinaryCipher().check_key(key):
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Цифры!!)")


            # проверерка на символы алфавита, пробелы, цифры и прочее

            binary = BinaryCipher(bit_size=6)

            binary_text = binary.text_to_binary(text)
            binary_key = binary.text_to_binary(key)

            self.text_box_top_right.delete("1.0", tk.END)
            self.text_box_top_right.insert(tk.END, binary_text)

            self.text_box_bot_right.delete("1.0", tk.END)
            self.text_box_bot_right.insert(tk.END, binary_key)

        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при бинаризации текста: {e}", )
            print(e)

    def encrypt_xor_by_key(self):
        try:
            binary_text = self.text_box_top_right.get("1.0", tk.END).strip()
            binary_key = self.text_box_bot_right.get("1.0", tk.END).strip()

            if binary_text=='' or binary_key=='':
                raise Exception(
                    "\nВы ещё не ввели текст и ключ или не выполнили процесс бинаризации\nбинарные слова должны быть из цифр 1 и 0")

            binary = BinaryCipher(bit_size=6)
            encrypted_text = binary.xor_with_key(binary_text=binary_text, binary_key=binary_key)
            self.mid_text_box.delete("1.0", tk.END)
            self.mid_text_box.insert(tk.END, encrypted_text)

        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при шифровке текста: {e}", )
            print(e)

    def decrypt_xor_by_key(self):
        try:
            encrypted_text = self.mid_text_box.get("1.0", tk.END).strip()
            binary_key = self.text_box_bot_right.get("1.0", tk.END).strip()

            if encrypted_text=='':
                raise Exception(
                    "\nВы ещё не провели процес XOR\nВыполните предыдущие шаги алгоритма!")

            binary = BinaryCipher(bit_size=6)
            encrypted_text = binary.xor_with_key(binary_text=encrypted_text, binary_key=binary_key)
            simple_text = binary.binary_to_text(encrypted_text)
            self.left_text_box.delete("1.0", tk.END)
            self.left_text_box.insert(tk.END, encrypted_text)
            self.right_text_box.delete("1.0", tk.END)
            self.right_text_box.insert(tk.END, simple_text)

        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при дешифровке текста: {e}", )
            print(e)

    def on_focus_out(self, event):
        self.entry_key.configure(state='normal')
        self.text_box.configure(state='normal')

    def on_focus_in(self, event):
        self.entry_key.configure(state='disabled')
        self.text_box.configure(state='disabled')

    def tab2_content(self):
        # Верхний фрейм с комбобоксами и полями ввода
        self.top_frame = tk.Frame(self.content_frame)
        self.top_frame.pack(pady=10)

        self.language_combo = ttk.Combobox(self.top_frame, values=["Русский", "Английский"])
        self.language_combo.pack(side=tk.LEFT, padx=5)
        self.language_combo.set("Выберите язык")

        self.binarization_button = tk.Button(self.top_frame, text="Почистить формочки", width=20,
                                             command=self.clean_tab_2)
        self.binarization_button.pack(pady=0)

        self.mid_framge = tk.Frame(self.content_frame)
        self.mid_framge.pack(pady=10)

        self.mid_frame_left = tk.Frame(self.mid_framge)
        self.mid_frame_left.pack(side=tk.LEFT, pady=10)

        self.mid_frame_right = tk.Frame(self.mid_framge)
        self.mid_frame_right.pack(side=tk.RIGHT, pady=10)

        # ScrolledText для ввода многострочного текста
        self.text_box_top_left = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_top_left.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_top_left.insert(tk.END, "Введите сюда сообщение")

        # ScrolledText для ввода многострочного текста
        self.text_box_top_right = scrolledtext.ScrolledText(self.mid_frame_right, height=3)
        self.text_box_top_right.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_top_right.insert(tk.END, "")

        # ScrolledText для ввода многострочного текста
        self.text_box_bot_left = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_bot_left.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_bot_left.insert(tk.END, "")

        self.generate_gamma_button = tk.Button(self.mid_frame_right, text="Генерация Гаммы", width=20,
                                             command=self.generate_gamma)
        self.generate_gamma_button.pack(pady=20)

        self.binarization_button = tk.Button(self.content_frame, text="Бинаризация", width=20,
                                             command=self.text_binarization_with_gamma)
        self.binarization_button.pack(pady=20)

        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        self.center_button_xor = tk.Button(self.content_frame, text="XOR", width=20,
                                           command=self.encrypt_xor_by_gamma)
        self.center_button_xor.pack(pady=20)

        self.mid_text_box = scrolledtext.ScrolledText(self.content_frame, height=3)
        self.mid_text_box.pack()
        self.mid_text_box.insert(tk.END, "")

        self.center_button_decrypt = tk.Button(self.content_frame, text="Расшифровать", width=20,
                                               command=self.decrypt_xor_by_gamma)
        self.center_button_decrypt.pack(pady=20)

        # Нижний фрейм с текстовыми полями и кнопками
        self.bottom_frame = tk.Frame(self.content_frame)
        self.bottom_frame.pack(pady=10)

        left_frame = tk.Frame(self.bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.left_text_box = scrolledtext.ScrolledText(left_frame, height=10, width=50)
        self.left_text_box.pack()
        self.left_text_box.insert(tk.END, "")

        right_frame = tk.Frame(self.bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        self.right_text_box = scrolledtext.ScrolledText(right_frame, height=10, width=50)
        self.right_text_box.pack()
        self.right_text_box.insert(tk.END, "")

    def generate_gamma(self):
        try:
            text = self.text_box_top_left.get("1.0", tk.END).strip()
            language = self.language_combo.get()
            if language not in ['Русский', 'Английский']:
                raise Exception('Вы не выбрали язык!\nВыберите его!!!')
            if text in ['' or 'Сюда введите сообщение']:
                raise Exception('Вы не ввели текст!\nВведите его!!!')
            if text != BinaryCipher().clean_string(text).lower():
                raise Exception(
                    "\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            if not BinaryCipher().check_alphabeta(text, _lang='ru' if language == "Русский" else 'en'):
                raise Exception(
                    "\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")
            if BinaryCipher().check_key(text):
                raise Exception(
                    "\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Цифры!!)")

            self.text_box_top_right.delete("1.0", tk.END)
            binary = BinaryCipher(bit_size=6)
            gamma = binary.generate_gamma(len(binary.text_to_binary(text)))
            self.text_box_top_right.insert(tk.END, gamma)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при генерации Гаммы: {e}", )
            print(e)

    def text_binarization_with_gamma(self):
        try:
            self.text_box_bot_left.delete("1.0", tk.END)
            text = self.text_box_top_left.get("1.0", tk.END).strip()
            language = self.language_combo.get()
            if language not in ['Русский', 'Английский']:
                raise Exception('Вы не выбрали язык!\nВыберите его!!!')
            if text in ['' or 'Сюда введите сообщение']:
                raise Exception('Вы не ввели текст!\nВведите его!!!')
            if text != BinaryCipher().clean_string(text).lower():
                raise Exception(
                    "\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            if not BinaryCipher().check_alphabeta(text, _lang='ru' if language == "Русский" else 'en'):
                raise Exception(
                    "\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")
            if BinaryCipher().check_key(text):
                raise Exception(
                    "\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Цифры!!)")

            binary = BinaryCipher(bit_size=6)
            binary_text = binary.text_to_binary(text)
            self.text_box_bot_left.insert(tk.END, binary_text)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при генерации Гаммы: {e}", )
            print(e)

    def encrypt_xor_by_gamma(self):
        try:
            binary_text = self.text_box_bot_left.get("1.0", tk.END).strip()
            gamma = self.text_box_top_right.get("1.0", tk.END).strip()

            if binary_text=='' or gamma=='':
                raise Exception(
                    "\nВаши поля пусты или не подходят\nВыполните предыдущие шаги алгоритма!")

            binary = BinaryCipher(bit_size=6)
            encrypted_text = binary.xor(binary_text, gamma)
            self.mid_text_box.delete("1.0", tk.END)
            self.mid_text_box.insert(tk.END, encrypted_text)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при XOR: {e}", )
            print(e)

    def decrypt_xor_by_gamma(self):
        try:
            encrypted_text = self.mid_text_box.get("1.0", tk.END).strip()
            binary_key = self.text_box_top_right.get("1.0", tk.END).strip()

            if encrypted_text == '' or binary_key == '':
                raise Exception(
                    "\nВаши поля пусты или не подходят\nВыполните предыдущие шаги алгоритма!")

            binary = BinaryCipher(bit_size=6)
            encrypted_text = binary.xor_with_key(binary_text=encrypted_text, binary_key=binary_key)
            simple_text = binary.binary_to_text(encrypted_text)
            self.left_text_box.delete("1.0", tk.END)
            self.left_text_box.insert(tk.END, encrypted_text)
            self.right_text_box.delete("1.0", tk.END)
            self.right_text_box.insert(tk.END, simple_text)

        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при расшифровке бинарного текста: {e}", )
            print(e)

    def clean_tab_1(self):
        self.language_combo.set("Выберите язык")
        self.text_box_top_left.delete("1.0", tk.END)
        self.text_box_top_left.insert(tk.END, "Сюда введите сообщение")

        self.text_box_bot_left.delete("1.0", tk.END)
        self.text_box_bot_left.insert(tk.END, "Сюда введите ключ")

        self.text_box_top_right.delete("1.0", tk.END)
        self.text_box_top_right.insert(tk.END, "")

        self.right_text_box.delete("1.0", tk.END)
        self.right_text_box.insert(tk.END, "")

        self.left_text_box.delete("1.0", tk.END)
        self.left_text_box.insert(tk.END, "")


        self.mid_text_box.delete("1.0", tk.END)
        self.mid_text_box.insert(tk.END, "")

        self.text_box_bot_right.delete("1.0", tk.END)
        self.text_box_bot_right.insert(tk.END, "")
    def clean_tab_2(self):
        pass
    def clean_tab_3(self):
        self.language_combo.set("Выберите язык")
        self.text_box_top_left.delete("1.0", tk.END)
        self.text_box_top_left.insert(tk.END, "Сюда введите сообщение")

        self.text_box_bot_left.delete("1.0", tk.END)
        self.text_box_bot_left.insert(tk.END, "Сюда введите ключ")

        self.text_box_top_right.delete("1.0", tk.END)
        self.text_box_top_right.insert(tk.END, "")

        self.text_box_gamma.delete("1.0", tk.END)
        self.text_box_gamma.insert(tk.END, "Тут будет ваша Гамма")

        self.mid_text_box_iv2.delete("1.0", tk.END)
        self.mid_text_box_iv2.insert(tk.END, "")

        self.mid_text_box.delete("1.0", tk.END)
        self.mid_text_box.insert(tk.END, "")

        self.left_text_box.delete("1.0", tk.END)
        self.left_text_box.insert(tk.END, "")

        self.right_text_box.delete("1.0", tk.END)
        self.right_text_box.insert(tk.END, "")







    def tab3_content(self):
        # Верхний фрейм с комбобоксами и полями ввода
        self.top_frame = tk.Frame(self.content_frame)
        self.top_frame.pack(pady=10)

        self.language_combo = ttk.Combobox(self.top_frame, values=["Русский", "Английский"])
        self.language_combo.pack(side=tk.LEFT, padx=5)
        self.language_combo.set("Выберите язык")

        self.binarization_button = tk.Button(self.top_frame, text="Почистить формочки", width=20,
                                             command=self.clean_tab_3)
        self.binarization_button.pack(pady=0)

        self.mid_framge = tk.Frame(self.content_frame)
        self.mid_framge.pack(pady=10)

        self.mid_frame_left = tk.Frame(self.mid_framge)
        self.mid_frame_left.pack(side=tk.LEFT, pady=10)

        self.mid_frame_right = tk.Frame(self.mid_framge)
        self.mid_frame_right.pack(side=tk.RIGHT, pady=10)

        # ScrolledText для ввода многострочного текста
        self.text_box_top_left = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_top_left.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_top_left.insert(tk.END, "Сюда введите сообщение")

        # ScrolledText для ввода многострочного текста
        self.text_box_top_right = scrolledtext.ScrolledText(self.mid_frame_right, height=3)
        self.text_box_top_right.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_top_right.insert(tk.END, "")

        # ScrolledText для ввода многострочного текста
        self.text_box_bot_left = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_bot_left.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_bot_left.insert(tk.END, "Сюда введите ключ")

        # ScrolledText для ввода многострочного текста
        self.text_box_bot_right = scrolledtext.ScrolledText(self.mid_frame_right, height=3)
        self.text_box_bot_right.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_bot_right.insert(tk.END, "")

        self.binarization_button = tk.Button(self.content_frame, text="Бинаризация", width=20,
                                             command=self.text_binarization)
        self.binarization_button.pack(pady=20)

        # ScrolledText для ввода многострочного текста
        self.text_box_gamma = scrolledtext.ScrolledText(self.mid_frame_left, height=3)
        self.text_box_gamma.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box_gamma.insert(tk.END, "Тут будет ваша Гамма")

        self.text_box_gamma_button = tk.Button(self.mid_frame_right, text="Генерация IV1", width=20,
                                             command=self.generate_gamma_as_iv1)
        self.text_box_gamma_button.pack(pady=20)

        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        self.center_button_iv2 = tk.Button(self.content_frame, text="Получить IV2", width=20,
                                           command=self.get_iv2)
        self.center_button_iv2.pack(pady=20)

        self.mid_text_box_iv2 = scrolledtext.ScrolledText(self.content_frame, height=3)
        self.mid_text_box_iv2.pack()
        self.mid_text_box_iv2.insert(tk.END, "")

        self.center_button_xor = tk.Button(self.content_frame, text="XOR", width=20,
                                           command=self.encrypt_xor_by_blocks)
        self.center_button_xor.pack(pady=20)

        self.mid_text_box = scrolledtext.ScrolledText(self.content_frame, height=3)
        self.mid_text_box.pack()
        self.mid_text_box.insert(tk.END, "")

        self.center_button_decrypt = tk.Button(self.content_frame, text="Расшифровать", width=20,
                                               command=self.decrypt_xor_by_blocks)
        self.center_button_decrypt.pack(pady=20)

        # Нижний фрейм с текстовыми полями и кнопками
        self.bottom_frame = tk.Frame(self.content_frame)
        self.bottom_frame.pack(pady=10)

        left_frame = tk.Frame(self.bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.left_text_box = scrolledtext.ScrolledText(left_frame, height=3, width=50)
        self.left_text_box.pack()
        self.left_text_box.insert(tk.END, "")

        right_frame = tk.Frame(self.bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        self.right_text_box = scrolledtext.ScrolledText(right_frame, height=3, width=50)
        self.right_text_box.pack()
        self.right_text_box.insert(tk.END, "")

    def generate_gamma_as_iv1(self):
        try:
            self.text_box_gamma.delete("1.0", tk.END)
            binary = BinaryCipher(bit_size=6)
            gamma = binary.generate_gamma(6)
            self.text_box_gamma.insert(tk.END, gamma)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при генерации Гаммы: {e}", )
            print(e)

    def get_iv2(self):
        try:
            self.mid_text_box_iv2.delete("1.0", tk.END)

            gamma = self.text_box_gamma.get("1.0", tk.END).strip()
            key = self.text_box_bot_right.get("1.0", tk.END).strip()

            if gamma in ['Тут будет ваша Гамма', '']:
                raise Exception('Вы ещё не сгенерировали Гамму IV1')

            if key in ['Сюда введите ключ', '']:
                raise Exception('Вы ещё не получили бинарное представление ключа!')

            iv2 = BinaryCipher(6).xor(gamma, key[-6:])
            self.mid_text_box_iv2.insert(tk.END, iv2)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при обработке IV2: {e}", )
            print(e)

    def encrypt_xor_by_blocks(self):
        try:
            iv2 = self.mid_text_box_iv2.get("1.0", tk.END).strip()
            bin_text = self.text_box_top_right.get("1.0", tk.END).strip()

            if iv2 =='':
                raise Exception('Вы ещё не сгенерировали IV2\nВыполните предыдущие шаги алгоритма')

            if bin_text in ['Сюда введите текст', '']:
                raise Exception('Вы ещё не получили бинарное представление текста!\nВыполните предыдущие шаги алгоритма')

            binary = BinaryCipher(6)
            blocks = binary.split_into_blocks(binary_text=bin_text, block_size=6)
            encryption_result = binary.xor_by_blocks(blocks, iv2)

            self.mid_text_box.delete("1.0", tk.END)
            self.mid_text_box.insert(tk.END, encryption_result["encrypted_message"])
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при XOR: {e}", )
            print(e)

    def decrypt_xor_by_blocks(self):
        try:
            iv2 = self.mid_text_box_iv2.get("1.0", tk.END).strip()
            bin_text = self.mid_text_box.get("1.0", tk.END).strip()

            if iv2 =='':
                raise Exception('Вы ещё не сгенерировали IV2\nВыполните предыдущие шаги алгоритма')

            if bin_text in ['Сюда введите текст', '']:
                raise Exception('Вы ещё не получили бинарное представление зашифрованного текста!\nВыполните предыдущие шаги алгоритма')


            text, binary_message = BinaryCipher(6).decrypt(encrypted_message=bin_text, iv2=iv2)

            self.left_text_box.delete("1.0", tk.END)
            self.left_text_box.insert(tk.END, text)

            self.right_text_box.delete("1.0", tk.END)
            self.right_text_box.insert(tk.END, binary_message)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Ошибка при расшифровке: {e}", )
            print(e)

    def hack_text_frame(self):
        try:
            text = self.text_box.get("1.0", tk.END).strip()
            language = self.combo1.get()
            # if language not in ['Русский', 'Английский']:
            #     raise Exception('Вы не выбрали язык!\nВыберите его!!!')
            # if text in ['', 'Тут будет ваш текст!']:
            #     raise Exception('Вы не ввели текст из текстового файла либо файл пуст!\nИсправляйте это недоразумение!')
            # if text != Vigenere().clean_string(text).lower():
            #     raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            # if not Vigenere().check_alphabeta(text, _lang='ru' if language=="Русский" else 'en'):
            #     raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")

            # vigenere = Vigenere()
            # decrypted_text, key = vigenere.decrypt_text(text=text, lang='ru' if language=='Русский' else 'en')
            ru_d = 43
            en_d = 36
            self.left_text_box.delete("1.0", tk.END)
            # messagebox.showinfo(title='Анализ',
            #                     message=f"При помощи метода индекса совпадений Фридмана был определен ключ шифрования!\n\n"
            #                             f"Ключ шифрования: {key}\n")
            # self.left_text_box.insert(tk.END, decrypted_text)
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Вы некорректно указали данные: {e}", )
            print(e)


    # Метод для загрузки текста из файла
    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                    # Изменяем состояние text_box
                    self.text_box.configure(state='normal')  # Включаем редактирование
                    self.text_box.delete("1.0", tk.END)  # Очищаем текст бокса
                    self.text_box.insert(tk.END, file_content)  # Вставляем новый текст
                    self.text_box.configure(state='disabled')  # Отключаем редактирование снова

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    # Метод для сохранения текста в файл
    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                text_to_save = self.left_text_box.get("1.0", tk.END).strip()
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_to_save)
                messagebox.showinfo("Успешно", "Текст успешно сохранен в файл")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def encrypt_text_frame_1(self):
        try:
            language = self.combo1.get()
            k = self.entry_key.get("1.0", tk.END).strip()
            # aspect = self.combo2.get()
            text = self.text_box.get("1.0", tk.END).strip()
            if language not in ['Русский', 'Английский']:
                raise Exception('Вы не выбрали язык!\nВыберите его!!!')
            if k.isdigit():
                raise Exception('\nВы не правильно указали ключ!\nКлюч должен быть словом(без цифр и прочего)\nИсправьтесь!')
            # if not k.isdigit():
            #     if Vigenere().check_key(k):
            #         raise Exception('\nВы не правильно указали улюч!\nВаш ключ cодержит цифры\nИсправьтесь!')
            #     if not Vigenere().check_alphabeta(k, 'ru' if language=='Русский' else 'en'):
            #         raise Exception('\nВы не правильно указали улюч!\nВаш ключ cодержит символы из стороннего алфавита\nИсправьтесь!')
            #     if not k == Vigenere().clean_string(k).lower():
            #         raise Exception('\nВы не правильно указали улюч!\nВаш ключ cодержит символы недоступные символы\nИсправьтесь!')
            #     if len(k) > len(text):
            #         messagebox.showinfo(title='Осторожно', message=f"Обращаю внимание на то, что длина вашего ключа превышает длину текста!\nПри шифровании будет использоваться лишь значимая часть ключа\nЕсли вас это не устраивает - измените текст или ключ!", )
            #         # raise Exception('\nВы не правильно указали улюч!\nДлина вашего ключа превышает длину текста!\nИсправьтесь!')


            if text in ['', 'Введите текст сюда!']:
                raise Exception('Вы не ввели текст в текстовое поле либо оно пустое!')
            if text in ['', 'Тут будет ваш текст!']:
                raise Exception('Вы не ввели текст из текстового файла либо файл пуст!\nИсправляйте это недоразумение!')
            # if text != Vigenere().clean_string(text).lower():
            #     raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            # if not Vigenere().check_alphabeta(text, _lang='ru' if language=="Русский" else 'en'):
            #     raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")

            # vigenere = Vigenere()
            # encr_text = vigenere.encrypt_text(text=text,
            #                              key=k,
            #                              language='ru' if language == 'Русский' else 'en')

            # Очищаем текстбоксы перед вставкой новых значений
            self.left_text_box.delete("1.0", tk.END)
            self.right_text_box.delete("1.0", tk.END)

            # Вставляем зашифрованный текст в левый
            # self.left_text_box.insert(tk.END, encr_text)
            self.right_text_box.insert(tk.END, '')
            self.center_button.config(text="Расшифровать", command=lambda: self.decrypt_text_frame_1(lang='ru' if language == 'Русский' else 'en'))
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Вы некорректно указали данные: {e}", )
            print(e)


    def decrypt_text_frame_1(self, lang):
        text_to_decrypt = self.left_text_box.get("1.0", tk.END).strip()
        key = self.entry_key.get("1.0", tk.END).strip()
        # alphabet = Vigenere().ru_dict if lang=='ru' else Vigenere().en_dict
        #
        # decrypted_text_vigenere = Vigenere().decrypt_vigenere(text=text_to_decrypt,
        #                                                       key=key,
        #                                                       alphabet=alphabet)
        # self.left_text_box.delete("1.0", tk.END)
        # self.right_text_box.delete("1.0", tk.END)
        self.left_text_box.insert(tk.END, '')
        # self.right_text_box.insert(tk.END, decrypted_text_vigenere)
        ru_d = 43
        en_d = 36
        messagebox.showinfo(title='Анализ',
                            message=f"Мы расшифровали текст, который ранее был зашифрован методом Виженера\n\n"
                                    f"Определен ключ шифрования: {key}")
        self.center_button.config(text="Зашифровать", command=self.encrypt_text_frame_1)

# Основной класс приложения
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Шифр Виженера")
        self.geometry("850x660")

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        self.tabs = TabButtons(self, self.content_frame)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
