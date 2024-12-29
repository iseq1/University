import re
import sys
from collections import Counter
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMainWindow, QFileDialog, QTextEdit, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import os
import string

ALPHABETS = {
    "Русский": "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я 0 1 2 3 4 5 6 7 8 9".split(),
    "Английский": "a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9".split()
}


class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шифр Цезаря")
        self.setGeometry(200, 200, 800, 800)

        # Создание вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Выбор алфавита на уровне всего приложения
        self.alphabet_choice = QComboBox()
        self.alphabet_choice.addItems(["Русский", "Английский"])
        self.alphabet_choice.currentIndexChanged.connect(self.update_validators)

        # Основной макет для выбора алфавита
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Выберите алфавит:"))
        main_layout.addWidget(self.alphabet_choice)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setMenuWidget(main_widget)

        # Вкладки для работы с текстом и файлами
        self.text_tab = TextTab(self.alphabet_choice)
        self.file_tab = FileTab(self.alphabet_choice)
        self.crack_tab = CrackTab(self.alphabet_choice)
        self.tabs.addTab(self.text_tab, "Шифр/Расшифр текста")
        self.tabs.addTab(self.file_tab, "Работа с файлами")
        self.tabs.addTab(self.crack_tab, "Взлом")

    def update_validators(self):
        # Обновляем валидаторы во всех табах
        self.text_tab.update_validator()
        self.file_tab.update_validator()
        self.crack_tab.update_validator()


class CipherOperations:
    @staticmethod
    def caesar_cipher(text, key, alphabet, decrypt=False):
        # key = key % len(alphabet)
        if decrypt:
            key = -key

        result = ""
        for char in text:
            idx = alphabet.index(char)
            new_idx = (idx + key) % len(alphabet)
            new_char = alphabet[new_idx]
            result += new_char
        return result

    @staticmethod
    def preprocess_text(text):
        # Обрабатываем только буквы и цифры, пробелы и знаки препинания оставляем как есть
        return ''.join(char.lower() if char.isalpha() or char.isdigit() else char for char in text)


class TextTab(QWidget, CipherOperations):
    def __init__(self, alphabet_choice):
        super().__init__()

        # Сохраняем ссылку на выбор алфавита
        self.alphabet_choice = alphabet_choice

        # Основной макет
        layout = QFormLayout()

        # Поле ввода для исходного сообщения
        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Введите исходное сообщение")
        layout.addRow(QLabel("Исходное сообщение:"), self.input_text)

        # Поле для ввода ключа
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Введите ключ (целое число)")
        layout.addRow(QLabel("Ключ:"), self.key_input)

        # Кнопка для шифрования
        self.encrypt_button = QPushButton("Зашифровать")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addRow(self.encrypt_button)

        # Кнопка для дешифрования
        self.decrypt_button = QPushButton("Расшифровать")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        layout.addRow(self.decrypt_button)

        # Поле для вывода результата
        self.output_text = QLabel("Результат:")
        layout.addRow(self.output_text)

        self.setLayout(layout)
        self.encrypted_text = ""  # Поле для хранения зашифрованного текста

        # Устанавливаем начальный валидатор
        self.update_validator()

        # Устанавливаем валидатор для поля ввода ключа
        self.setup_key_validator()

    def update_validator(self):
        alphabet = ALPHABETS[self.alphabet_choice.currentText()]

        regex = QRegExp(f"[{''.join(alphabet)}{''.join(c.upper() for c in alphabet)}]*")

        validator = QRegExpValidator(regex)

        self.input_text.setValidator(validator)

        self.input_text.clear()

    def setup_key_validator(self):
        # Валидатор для поля ввода ключа, разрешающий только цифры
        regex = QRegExp(r"-?\d*")
        validator = QRegExpValidator(regex)
        self.key_input.setValidator(validator)

    def encrypt_text(self):
        try:
            text = self.input_text.text()
            if not text:
                self.output_text.setText("Ошибка: введите текст для шифрования.")
                self.encrypted_text = ""
                return

            key = int(self.key_input.text())
            alphabet = ALPHABETS[self.alphabet_choice.currentText()]
            processed_text = self.preprocess_text(text)
            self.encrypted_text = self.caesar_cipher(processed_text, key, alphabet)
            self.output_text.setText(f"Зашифрованное сообщение: {self.encrypted_text}")
        except ValueError:
            self.output_text.setText("Ошибка: ключ должен быть целым числом.")
            self.encrypted_text = ""

    def decrypt_text(self):
        try:
            if not self.encrypted_text:
                self.output_text.setText("Ошибка: нет текста для расшифровки.")
                self.encrypted_text = ""
                return

            key = int(self.key_input.text())
            alphabet = ALPHABETS[self.alphabet_choice.currentText()]
            processed_text = self.preprocess_text(self.encrypted_text)
            decrypted_text = self.caesar_cipher(processed_text, key, alphabet, decrypt=True)
            self.output_text.setText(f"Расшифрованное сообщение: {decrypted_text}")
        except ValueError:
            self.output_text.setText("Ошибка: ключ должен быть целым числом.")
            self.encrypted_text = ""


class FileTab(QWidget, CipherOperations):
    def __init__(self, alphabet_choice):
        super().__init__()
        self.alphabet_choice = alphabet_choice
        layout = QVBoxLayout()

        # Кнопка выбора файла
        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.open_file)
        layout.addWidget(self.file_button)

        # Поле для отображения текста из файла
        self.file_text_display = QTextEdit()
        self.file_text_display.setReadOnly(True)
        layout.addWidget(self.file_text_display)

        # Поле для ввода ключа
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Введите ключ (целое число)")
        layout.addWidget(QLabel("Ключ:"))
        layout.addWidget(self.key_input)

        # Кнопка для шифрования
        self.encrypt_button = QPushButton("Зашифровать")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        layout.addWidget(self.encrypt_button)

        # Поле для отображения зашифрованного текста
        self.encrypted_text_display = QTextEdit()
        self.encrypted_text_display.setReadOnly(True)
        layout.addWidget(QLabel("Зашифрованный текст:"))
        layout.addWidget(self.encrypted_text_display)

        # Кнопка для расшифровки текста
        self.decrypt_button = QPushButton("Расшифровать")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        layout.addWidget(self.decrypt_button)

        # Поле для отображения расшифрованного текста
        self.decrypted_text_display = QTextEdit()
        self.decrypted_text_display.setReadOnly(True)
        layout.addWidget(QLabel("Расшифрованный текст:"))
        layout.addWidget(self.decrypted_text_display)

        # Кнопка для сохранения зашифрованного текста
        self.save_button = QPushButton("Сохранить в файл (Зашифрованный текст)")
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.file_text = ""
        self.encrypted_text = ""
        self.decrypted_text = ""

        # Устанавливаем валидатор для поля ввода ключа
        self.setup_key_validator()

    def setup_key_validator(self):
        # Валидатор для поля ввода ключа, разрешающий только цифры
        regex = QRegExp(r"-?\d*")
        validator = QRegExpValidator(regex)
        self.key_input.setValidator(validator)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.txt);")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.file_text = file.read()

            if all(char.lower() in string.punctuation + " " + "\n—" for char in self.file_text):
                self.file_text_display.setText("Ошибка: некорректный текст.")
                self.file_text = ""

            # Проверяем соответствие языка
            elif self.is_valid_text():
                self.file_text_display.setPlainText(self.file_text)
            else:
                self.file_text_display.setPlainText("Ошибка: текст не соответствует выбранному языку.")
                self.file_text = ""
                self.decrypted_text_display.setPlainText("")
                self.encrypted_text_display.setPlainText("")
                self.key_input.clear()
                self.decrypted_text = ""
                self.encrypted_text = ""

    def is_valid_text(self):
        alphabet = ALPHABETS[self.alphabet_choice.currentText()]
        return all(char.lower() in alphabet for char in self.file_text)

    def update_validator(self):
        self.file_text_display.clear()
        self.encrypted_text_display.clear()
        self.file_text = ""
        self.encrypted_text = ""
        self.decrypted_text = ""
        self.decrypted_text_display.clear()
        self.key_input.clear()

    def encrypt_text(self):
        try:
            if self.file_text == "" or self.file_text == '':
                self.encrypted_text_display.setPlainText("Ошибка: текст не выбран.")
            else:
                key = int(self.key_input.text())
                alphabet = ALPHABETS[self.alphabet_choice.currentText()]
                processed_text = self.preprocess_text(self.file_text)
                self.encrypted_text = self.caesar_cipher(processed_text, key, alphabet)
                self.encrypted_text_display.setPlainText(self.encrypted_text)
        except ValueError:
            self.encrypted_text_display.setPlainText("Ошибка: ключ должен быть целым числом.")

    def decrypt_text(self):
        try:
            if self.encrypted_text == "" or self.encrypted_text == '':
                self.decrypted_text_display.setPlainText("Ошибка: зашифрованный текст не выбран.")
            else:
                key = int(self.key_input.text())
                alphabet = ALPHABETS[self.alphabet_choice.currentText()]
                self.decrypted_text = self.caesar_cipher(self.encrypted_text, key, alphabet, decrypt=True)
                self.decrypted_text_display.setPlainText(self.decrypted_text)
        except ValueError:
            self.decrypted_text_display.setPlainText("Ошибка: ключ должен быть целым числом.")

    def save_file(self):
        if self.decrypted_text == "" or self.decrypted_text == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка: зашифрованный текст не выбран.")
            msg.setWindowTitle("Предупреждение")
            msg.exec_()
        else:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.encrypted_text)


class CrackTab(QWidget):
    def __init__(self, alphabet_choice):
        super().__init__()
        self.alphabet_choice = alphabet_choice
        layout = QVBoxLayout()

        # Кнопка для выбора файла
        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.open_file)
        layout.addWidget(self.file_button)

        # Поле для отображения зашифрованного текста
        self.encrypted_text_display = QTextEdit()
        self.encrypted_text_display.setReadOnly(True)
        layout.addWidget(QLabel("Зашифрованный текст:"))
        layout.addWidget(self.encrypted_text_display)

        # Кнопка для взлома
        self.crack_button = QPushButton("Взломать")
        self.crack_button.clicked.connect(self.crack_text)
        layout.addWidget(self.crack_button)

        # Поле для отображения предполагаемого ключа
        self.key_display = QLabel("Предполагаемый ключ: ")
        layout.addWidget(self.key_display)

        # Поле для отображения расшифрованного текста
        self.decrypted_text_display = QTextEdit()
        self.decrypted_text_display.setReadOnly(True)
        layout.addWidget(QLabel("Дешифрованный текст:"))
        layout.addWidget(self.decrypted_text_display)

        self.setLayout(layout)

        self.file_text = ""

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Text Files (*.txt);")
        if file_path:
            # if self.is_valid_file(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                self.file_text = file.read()

            if all(char.lower() in string.punctuation + " " + "\n—" for char in self.file_text):
                self.encrypted_text_display.setText("Ошибка: некорректный текст.")
                self.file_text = ""

            # Проверка валидности текста
            elif self.is_valid_text():
                self.encrypted_text_display.setPlainText(self.file_text)
            else:
                self.encrypted_text_display.setText("Ошибка: текст не соответствует выбранному языку.")
                self.file_text = ""
                self.key_display.setText("Предполагаемый ключ: ")
                self.decrypted_text_display.setPlainText("")
        # else:
        #     self.encrypted_text_display.setText("Ошибка: файл не соответствует требуемому формату (должен начинаться с 'shifr' + цифра и заканчиваться на '.txt').")

    def is_valid_file(self, file_path):
        # Проверяем, что имя файла соответствует формату 'shifr' + цифра + '.txt'
        file_name = file_path.split("/")[-1]  # Извлекаем имя файла
        return bool(re.match(r"^shifr\d+\.txt$", file_name))

    def is_valid_text(self):
        alphabet = ALPHABETS[self.alphabet_choice.currentText()]
        return all(char.lower() in alphabet for char in self.file_text)

    def update_validator(self):
        self.encrypted_text_display.clear()
        self.file_text = ""
        self.key_display.setText("Предполагаемый ключ: ")
        self.decrypted_text_display.clear()

    def crack_text(self):
        if not self.file_text:
            self.decrypted_text_display.setPlainText("Ошибка: не выбран файл для взлома.")
            self.key_display.setText("Предполагаемый ключ: ")
            return

        text = CipherOperations.preprocess_text(self.file_text)
        alphabet = ALPHABETS[self.alphabet_choice.currentText()]

        # Частотный анализ
        freq = self.frequency_analysis(text, alphabet)

        # Находим наиболее частые символы
        sorted_freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)
        most_frequent_chars = [char for char, _ in sorted_freq[:3]]  # Топ-3 частых символа

        assumed_common_chars = ['о', 'е', 'а'] if self.alphabet_choice.currentText() == "Русский" else ['e', 't', 'a']

        # Перебор возможных ключей по самым частым символам
        for common_char in assumed_common_chars:
            for encrypted_char in most_frequent_chars:
                try:
                    key = (alphabet.index(encrypted_char) - alphabet.index(common_char))

                    # Дешифровка с найденным ключом
                    decrypted_text = CipherOperations.caesar_cipher(text, key, alphabet, decrypt=True)

                    if self.is_meaningful(decrypted_text):
                        self.key_display.setText(f"Предполагаемый ключ: {key}")
                        self.decrypted_text_display.setPlainText(decrypted_text)
                        return
                except ValueError:
                    continue

        self.decrypted_text_display.setPlainText("Ключ не найден. Попробуйте другой метод.")

    def frequency_analysis(self, text, alphabet):
        freq = {char: 0 for char in alphabet}
        for char in text:
            if char in freq:
                freq[char] += 1
        return freq

    def is_meaningful(self, text):
        common_words = {"the", "and", "in"} if self.alphabet_choice.currentText() == "Английский" else {"и", "в", "на"}
        return any(word in text for word in common_words)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec_())


