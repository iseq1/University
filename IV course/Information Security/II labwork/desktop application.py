import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from Vigenere import Vigenere
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
        # Верхний фрейм с комбобоксами и полем ввода
        self.top_frame = tk.Frame(self.content_frame)
        self.top_frame.pack(pady=10)

        self.combo1 = ttk.Combobox(self.top_frame, values=["Русский", "Английский"])
        self.combo1.pack(side=tk.LEFT, padx=5)
        self.combo1.set("Выберите язык")


        self.entry_key = scrolledtext.ScrolledText(self.top_frame, height=1, width=30)
        self.entry_key.pack(side=tk.LEFT, padx=5)
        self.entry_key.insert(tk.END, "Сюда введите свой ключик!")
        # self.entry_key.bind("<FocusIn>", self.on_focus_in)


        # self.combo2 = ttk.Combobox(self.top_frame, values=["Вправо", "Влево"])
        # self.combo2.pack(side=tk.LEFT, padx=5)
        # self.combo2.set("Выберите направление")

        # ScrolledText для ввода многострочного текста
        self.text_box = scrolledtext.ScrolledText(self.content_frame, height=12)
        self.text_box.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box.insert(tk.END, "Введите текст сюда")

        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Нижний фрейм с текстовыми полями и кнопками
        self.bottom_frame = tk.Frame(self.content_frame)
        self.bottom_frame.pack(pady=10)

        left_frame = tk.Frame(self.bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.left_text_box = scrolledtext.ScrolledText(left_frame, height=15, width=40)
        self.left_text_box.pack()
        self.left_text_box.insert(tk.END, "")

        right_frame = tk.Frame(self.bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        self.right_text_box = scrolledtext.ScrolledText(right_frame, height=15, width=45)
        self.right_text_box.pack()
        self.right_text_box.insert(tk.END, "")

        self.center_button = tk.Button(self.content_frame, text="Зашифровать", width=20, command=self.encrypt_text_frame_1)
        self.center_button.pack(pady=20)


    def on_focus_out(self, event):
        # self.entry_key.configure(state='normal')
        self.text_box.configure(state='normal')


    def on_focus_in(self, event):
        # self.entry_key.configure(state='disabled')
        self.text_box.configure(state='disabled')

    def tab2_content(self):
        # Верхний фрейм с комбобоксами и полем ввода
        self.top_frame = tk.Frame(self.content_frame)
        self.top_frame.pack(pady=10)

        # Комбобокс выбора языка
        self.combo1 = ttk.Combobox(self.top_frame, values=["Русский", "Английский"])
        self.combo1.pack(side=tk.LEFT, padx=5)
        self.combo1.set("Выберите язык")

        # Кнопка для выбора файла
        self.load_file_button = tk.Button(self.top_frame, text="Выбрать файл", command=self.load_file)
        self.load_file_button.pack(side=tk.LEFT, padx=5)


        # Поле ввода числа (сдвига k)
        self.entry_key = scrolledtext.ScrolledText(self.top_frame, height=1, width=30)
        self.entry_key.pack(side=tk.LEFT, padx=5)
        self.entry_key.insert(tk.END, "Сюда введите свой ключик!")
        # self.entry_key.bind("<FocusIn>", self.on_focus_in)
        # self.entry_key.bind("<FocusOut>", self.on_focus_out)

        # Комбобокс выбора направления
        # self.combo2 = ttk.Combobox(self.top_frame, values=["Вправо", "Влево"])
        # self.combo2.pack(side=tk.LEFT, padx=5)
        # self.combo2.set("Выберите направление")

        # ScrolledText для ввода многострочного текста
        self.text_box = scrolledtext.ScrolledText(self.content_frame, height=12)
        self.text_box.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box.insert(tk.END, "Тут будет ваш текст!")
        self.text_box.bind("<FocusIn>", self.on_focus_in)


        # Разделитель
        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Нижний фрейм с текстовыми полями и кнопками
        self.bottom_frame = tk.Frame(self.content_frame)
        self.bottom_frame.pack(pady=10)

        # Левый фрейм
        left_frame = tk.Frame(self.bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.left_text_box = scrolledtext.ScrolledText(left_frame, height=15, width=40)
        self.left_text_box.pack()
        self.left_text_box.insert(tk.END, "")

        # Правый фрейм
        right_frame = tk.Frame(self.bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        self.right_text_box = scrolledtext.ScrolledText(right_frame, height=15, width=40)
        self.right_text_box.pack()
        self.right_text_box.insert(tk.END, "")

        # Центральная кнопка "Зашифровать" и кнопка "Сохранить"
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        self.center_button = tk.Button(button_frame, text="Зашифровать", width=20, command=self.encrypt_text_frame_1)
        self.center_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для сохранения текста из правого текстбокса в файл
        self.save_button = tk.Button(button_frame, text="Сохранить в файл", width=20, command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

    def tab3_content(self):
        # Верхний фрейм с комбобоксами и полем ввода
        self.top_frame = tk.Frame(self.content_frame)
        self.top_frame.pack(pady=10)

        # Комбобокс выбора языка
        self.combo1 = ttk.Combobox(self.top_frame, values=["Русский", "Английский"])
        self.combo1.pack(side=tk.LEFT, padx=5)
        self.combo1.set("Выберите язык")

        # Кнопка для выбора файла
        self.load_file_button = tk.Button(self.top_frame, text="Выбрать файл", command=self.load_file)
        self.load_file_button.pack(side=tk.LEFT, padx=5)

        # Поле ввода числа (сдвига k)
        # self.entry_key = ttk.Entry(self.top_frame, width=10)
        # self.entry_key.pack(side=tk.LEFT, padx=5)
        # self.entry_key.insert(0, "k")

        # Комбобокс выбора направления
        # self.combo2 = ttk.Combobox(self.top_frame, values=["Вправо", "Влево"])
        # self.combo2.pack(side=tk.LEFT, padx=5)
        # self.combo2.set("Выберите направление")

        # ScrolledText для ввода многострочного текста
        self.text_box = scrolledtext.ScrolledText(self.content_frame, height=12)
        self.text_box.pack(pady=10, padx=10, fill=tk.BOTH)
        self.text_box.insert(tk.END, "Тут будет ваш текст!")
        self.text_box.configure(state='disabled')  # Отключаем редактирование снова

        # Разделитель
        separator = ttk.Separator(self.content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)

        # Нижний фрейм с текстовыми полями и кнопками
        self.bottom_frame = tk.Frame(self.content_frame)
        self.bottom_frame.pack(pady=10)

        # Левый фрейм
        left_frame = tk.Frame(self.bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        self.left_text_box = scrolledtext.ScrolledText(left_frame, height=15, width=40)
        self.left_text_box.pack()
        self.left_text_box.insert(tk.END, "")

        # Правый фрейм
        # right_frame = tk.Frame(self.bottom_frame)
        # right_frame.pack(side=tk.RIGHT, padx=10)
        #
        # self.right_text_box = scrolledtext.ScrolledText(right_frame, height=15, width=45)
        # self.right_text_box.pack()
        # self.right_text_box.insert(tk.END, "")

        # Центральная кнопка "Зашифровать" и кнопка "Сохранить"
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        self.center_button = tk.Button(button_frame, text="Взломать", width=20, command=self.hack_text_frame)
        self.center_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для сохранения текста из правого текстбокса в файл
        self.save_button = tk.Button(button_frame, text="Сохранить в файл", width=20, command=self.save_to_file)
        self.save_button.pack(side=tk.LEFT, padx=5)

    def hack_text_frame(self):
        try:
            text = self.text_box.get("1.0", tk.END).strip()
            language = self.combo1.get()
            if language not in ['Русский', 'Английский']:
                raise Exception('Вы не выбрали язык!\nВыберите его!!!')
            if text in ['', 'Тут будет ваш текст!']:
                raise Exception('Вы не ввели текст из текстового файла либо файл пуст!\nИсправляйте это недоразумение!')
            if text != Vigenere().clean_string(text).lower():
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            if not Vigenere().check_alphabeta(text, _lang='ru' if language=="Русский" else 'en'):
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")

            vigenere = Vigenere()
            decrypted_text, key = vigenere.decrypt_text(text=text, lang='ru' if language=='Русский' else 'en')
            ru_d = 43
            en_d = 36
            self.left_text_box.delete("1.0", tk.END)
            # self.right_text_box.delete("1.0", tk.END)
            messagebox.showinfo(title='Анализ',
                                message=f"При помощи метода индекса совпадений Фридмана был определен ключ шифрования!\n\n"
                                        f"Ключ шифрования: {key}\n")
            self.left_text_box.insert(tk.END, decrypted_text)
            # self.right_text_box.insert(tk.END, full_decrypted_text)
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
            print(k)
            # aspect = self.combo2.get()
            text = self.text_box.get("1.0", tk.END).strip()
            if language not in ['Русский', 'Английский']:
                raise Exception('Вы не выбрали язык!\nВыберите его!!!')
            if k.isdigit():
                raise Exception('\nВы не правильно указали ключ!\nКлюч должен быть словом(без цифр и прочего)\nИсправьтесь!')
            if not k.isdigit():
                if Vigenere().check_key(k):
                    raise Exception('\nВы не правильно указали улюч!\nВаш ключ cодержит цифры\nИсправьтесь!')
                if not Vigenere().check_alphabeta(k, 'ru' if language=='Русский' else 'en'):
                    raise Exception('\nВы не правильно указали улюч!\nВаш ключ cодержит символы из стороннего алфавита\nИсправьтесь!')
                if not k == Vigenere().clean_string(k).lower():
                    raise Exception('\nВы не правильно указали улюч!\nВаш ключ cодержит символы недоступные символы\nИсправьтесь!')
                if len(k) > len(text):
                    messagebox.showinfo(title='Осторожно', message=f"Обращаю внимание на то, что длина вашего ключа превышает длину текста!\nПри шифровании будет использоваться лишь значимая часть ключа\nЕсли вас это не устраивает - измените текст или ключ!", )
                    # raise Exception('\nВы не правильно указали улюч!\nДлина вашего ключа превышает длину текста!\nИсправьтесь!')


            if text in ['', 'Введите текст сюда!']:
                raise Exception('Вы не ввели текст в текстовое поле либо оно пустое!')
            if text in ['', 'Тут будет ваш текст!']:
                raise Exception('Вы не ввели текст из текстового файла либо файл пуст!\nИсправляйте это недоразумение!')
            if text != Vigenere().clean_string(text).lower():
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Пробелы, заглавные символы, знаки препинания)")
            if not Vigenere().check_alphabeta(text, _lang='ru' if language=="Русский" else 'en'):
                raise Exception("\nВы ввели инородные символы для алфавита в текстовое поле!!!\nИзбавьтесь от них:\n(Знаки из другого алфавита!!)")

            vigenere = Vigenere()
            encr_text = vigenere.encrypt_text(text=text,
                                         key=k,
                                         language='ru' if language == 'Русский' else 'en')

            # Очищаем текстбоксы перед вставкой новых значений
            self.left_text_box.delete("1.0", tk.END)
            self.right_text_box.delete("1.0", tk.END)

            # Вставляем зашифрованный текст в левый
            self.left_text_box.insert(tk.END, encr_text)
            self.right_text_box.insert(tk.END, '')
            self.center_button.config(text="Расшифровать", command=lambda: self.decrypt_text_frame_1(lang='ru' if language == 'Русский' else 'en', key=k))
        except Exception as e:
            messagebox.showinfo(title='Ошибка', message=f"Вы некорректно указали данные: {e}", )
            print(e)


    def decrypt_text_frame_1(self, lang, key):
        self.right_text_box.delete("1.0", tk.END)
        text_to_decrypt = self.left_text_box.get("1.0", tk.END).strip()
        key = key
        alphabet = Vigenere().ru_dict if lang=='ru' else Vigenere().en_dict

        decrypted_text_vigenere = Vigenere().decrypt_vigenere(text=text_to_decrypt,
                                                              key=key,
                                                              alphabet=alphabet)
        # self.left_text_box.delete("1.0", tk.END)
        # self.right_text_box.delete("1.0", tk.END)
        self.left_text_box.insert(tk.END, '')
        self.right_text_box.insert(tk.END, decrypted_text_vigenere)
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
