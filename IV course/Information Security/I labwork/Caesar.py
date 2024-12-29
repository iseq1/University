import math
from collections import Counter

class Caesar():

    def __init__(self, len_text):
        self.len_text = len_text
        self.text = None
        self.k = 0
        self.aspect = None
        self.lang = None
        self.SIL = None
        self.ru_dict = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + '0123456789'
        self.en_dict = "abcdefghijklmnopqrstuvwxyz" + '0123456789'
        # self.digit_dict = '0123456789'
        self.freq_ru = {
            'о': 10.97, 'е': 8.45, 'а': 8.01, 'и': 7.35, 'н': 6.7,
            'т': 6.26, 'с': 5.47, 'р': 4.73, 'в': 4.54, 'л': 4.4,
            'к': 3.49, 'м': 3.21, 'д': 2.98, 'п': 2.81, 'у': 2.62,
            'я': 2.01, 'ы': 1.9, 'ь': 1.74, 'г': 1.7, 'з': 1.65,
            'б': 1.59, 'ч': 1.44, 'й': 1.21, 'х': 0.97, 'ж': 0.94,
            'ш': 0.73, 'ю': 0.64, 'ц': 0.48, 'щ': 0.36, 'э': 0.32,
            'ф': 0.26, 'ъ': 0.04, 'ё': 0.02
        }
        self.freq_en = {
            'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0,
            'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3,
            'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4, 'w': 2.4,
            'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5
        }

    def clean_string(self, input_string):
        # Удаляем знаки препинания, но оставляем цифры
        cleaned_string = ''.join(char for char in input_string if char.isalnum() or char.isspace())
        cleaned_string = cleaned_string.replace(" ", "").replace('\n', '').replace('\r','')
        return cleaned_string

    def spaces_counter(self, text, _dict):
        spaces_index_list = {}
        for i in range(len(text)):
            char = text[i]

            # Проверка на заглавные буквы
            if char not in _dict:
                if char.lower() in _dict:
                    # Заглавные буквы фиксируем как "Upper"
                    spaces_index_list[i] = "Upper"
                # Запись переноса строки без маркировки заглавной буквы
                elif char == '\n' or char == '\r':
                    spaces_index_list[i] = char
                else:
                    # Другие символы (знаки препинания) оставляем как есть
                    spaces_index_list[i] = char

        return spaces_index_list

    def check_alphabeta(self, _text=None, _lang=None):
        if _text == None:
            text = self.text
        else:
            text=_text

        ru_range = set(self.ru_dict)
        en_range = set(self.en_dict)
        contains_ru = any(char in ru_range for char in text if char not in '0123456789')
        contains_en = any(char in en_range for char in text if char not in '0123456789')

        if contains_ru and contains_en:
            print('Тут есть и рус и англ')
            return False

        if _lang is not None:
            if contains_ru and _lang !='ru':
                print('Тут рус но выбрали en')
                return False
            if contains_en and _lang !='en':
                print('Тут англ но выбрали ru')
                return False

        return True


    def encrypt_text(self, text, k, aspect, lang):
        try:
            if lang == 'ru':
                _dict = self.ru_dict
            elif lang == 'en':
                _dict = self.en_dict
            else:
                raise Exception('Неизвестный словарь!')

            if not text:
                raise Exception('Вы не указали текст вовсе!')
            # тут надо строку преобразовать в большой инт
            # Индексы пробелов, знаков припенания и заглавных букв
            spaces_index_list = self.spaces_counter(text, _dict)
            new_text = self.clean_string(text)
            encrypted_text = ''
            self.check_alphabeta(new_text)
            k = int(k)
            if aspect == 'right':
                pass
            elif aspect == 'left':
                k *= -1
            else:
                raise Exception('Неверно указан вектор сдвига')

            for sign in range(len(new_text)):
                index = (_dict.find(new_text[sign].lower()) + k) % len(_dict)
                encrypted_text += (_dict[index])

            full_encrypted_text = ''
            encrypted_char_index = 0

            for i in range(len(text)):
                if i in spaces_index_list:
                    if spaces_index_list[i] == 'Upper':
                        full_encrypted_text += (encrypted_text[encrypted_char_index].upper())  # Добавляем оригинальный символ
                        encrypted_char_index += 1
                    else:
                        full_encrypted_text += (spaces_index_list[i])  # Добавляем оригинальный символ
                else:
                    full_encrypted_text += (encrypted_text[encrypted_char_index])  # Добавляем зашифрованный символ
                    encrypted_char_index += 1
            self.text = encrypted_text
            self.aspect = aspect
            self.lang = lang
            self.SIL = spaces_index_list

            return encrypted_text, full_encrypted_text
        except Exception as e:
            print(f'Ошибка при шифровании: {e}')

    def get_frequencies(self, _text=None, _lang=None):
        """
        Подсчет частот букв в тексте с учетом алфавита.
        """
        text = _text if _text is not None else self.text
        lang = _lang if _lang is not None else self.lang
        if text is None:
            raise ValueError("Текст не установлен. Пожалуйста, сначала зашифруйте текст или передайте значение _text.")

        # Удаляем цифры из текста
        text = ''.join(char for char in text if not char.isdigit())
        alphabet = self.ru_dict if lang == 'ru' else self.en_dict
        counter = Counter([char for char in text.lower() if char in alphabet])
        total = sum(counter.values())

        # Если в тексте нет букв из алфавита, возвращаем нулевые частоты
        if total == 0:
            return {char: 0 for char in alphabet}

        # Частоты всех букв алфавита
        frequencies = {char: (counter.get(char, 0) / total) * 100 for char in alphabet}
        return frequencies

    def find_shift(self, encrypted_freq, _lang=None):
        lang = _lang if _lang is not None else self.lang
        freq_table = self.freq_ru if lang == 'ru' else self.freq_en
        alphabet = self.ru_dict if lang == 'ru' else self.en_dict
        n = len(alphabet)

        # Список разниц для каждого сдвига
        differences = []

        # Перебираем все возможные сдвиги
        for shift in range(n):
            total_diff = 0

            # Рассчитываем разницу частот
            for i, char in enumerate(alphabet):
                # Определяем индекс со сдвигом
                shifted_char = alphabet[(i + shift) % n]
                expected_freq = freq_table.get(char, 0)
                actual_freq = encrypted_freq.get(shifted_char, 0)

                # Суммируем абсолютные разницы
                total_diff += abs(expected_freq - actual_freq)

            differences.append((shift, total_diff))

        best_shift = min(differences, key=lambda x: x[1])[0]

        return best_shift

    def decrypt_text_by_key(self, text, key, lang):
        lang = 'ru' if lang == 'Русский' else 'en'
        n = len(self.ru_dict) if lang == 'ru' else len(self.en_dict)
        pass


    def decrypt_text(self, text=None, spaces_index_list=None, lang=None):
        if text is None:
            text = self.text
        if lang is None:
            lang = self.lang
        else:
            lang = 'ru' if lang == 'Русский' else 'en'

        if spaces_index_list is None:
            spaces_index_list = self.SIL if self.SIL is not None else self.spaces_counter(
                text=text, _dict=self.ru_dict if lang == 'ru' else self.en_dict
            )

        # Получаем частоты букв в зашифрованном тексте
        freq = self.get_frequencies(_text=self.clean_string(text).lower(), _lang=lang)
        shift = self.find_shift(freq, _lang=lang)

        n = len(self.ru_dict) if lang == 'ru' else len(self.en_dict)

        # Определяем направление и величину сдвига
        if shift > n // 2:  # Если shift больше половины длины алфавита, сдвиг влево
            aspect = 'left'
            k = n - shift
        else:  # Иначе сдвиг вправо
            aspect = 'right'
            k = shift

        print(f"Определенные параметры: aspect={aspect}, k={k}")

        # Расшифровка текста
        decrypted_text, _ = self.encrypt_text(
            text=text,
            k=k,
            lang=lang,
            aspect='right' if aspect=='left' else 'left'
        )

        full_decrypted_text = ''
        decrypted_char_index = 0

        # Восстановление оригинального текста с пробелами и заглавными буквами
        for i in range(self.len_text):
            if i in spaces_index_list:
                if spaces_index_list[i] == 'Upper':
                    full_decrypted_text += decrypted_text[decrypted_char_index].upper()
                    decrypted_char_index += 1
                else:
                    full_decrypted_text += spaces_index_list[i]
            else:
                if decrypted_char_index < len(decrypted_text):
                    full_decrypted_text += decrypted_text[decrypted_char_index]
                    decrypted_char_index += 1

        return decrypted_text, full_decrypted_text, k, aspect

