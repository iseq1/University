from collections import Counter

class Vigenere():

    def __init__(self):
        self.ru_dict = ("абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + '0123456789')
        self.en_dict = ("abcdefghijklmnopqrstuvwxyz"  + '0123456789')
        self.IC_opentext_en = 0.0644
        self.IC_opentext_ru = 0.0553
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

    def encrypt_text(self, text, key, language):
        # Формула c_n = (Q + m_n + k_n) % Q
        # m_n - позиция символа открытого текста,
        # k_n - позиция символа ключа шифрования,
        # Q - количество символов в алфавите,
        # c_n - позиция символа зашифрованного текста.
        try:
            # Проверка на вшивость
            if text != self.clean_string(text):
                raise Exception("В вашем тексте сторонние символы!\nУдалите знаки препинания/заглавные буквы/пробелы")
            if not self.check_alphabeta(text, language):
                raise Exception("В вашем тексте сторонние символы!\nПроверьте ваш текст и выбранный вами алфавит!")
            if self.check_key(key) or not self.check_alphabeta(key, language) or key != self.clean_string(key):
                raise Exception("Ваш ключ не удовлетворяет условиям!\n1.Ключ исключает содержание цифр\n2.Символы ключа соответсвуют выбранному алфавиту\n3.Ключ не содержит иннородные символы ")

            # Определение ключика
            if len(key) < len(text):
                key_line = key * (len(text)//len(key)) + key[:len(text)%len(key)]
            elif len(key) == len(text):
                key_line = key
            else:
                # Тут надо понять, либо ключ сократить, либо ошибку выдать что key > text
                key_line = key[:len(text)]

            # Шифруем
            _dict = self.ru_dict if language == 'ru' else self.en_dict
            encrypted_text = ''
            for i in range(len(text)):
                char_index = _dict.find(text[i])
                key_index = _dict.find(key_line[i])
                if char_index == -1 or key_index == -1:
                    raise Exception("Шифровальная машина обнаружила ошибку!\nАлгоритм не обнаружил соответсвующий символ в нужном словаре\nСкорее всего ваша оплошность при вводе данных прошла через проверку данных незамеченной!")
                encrypted_char_index = (char_index + key_index) % len(_dict)
                encrypted_text += _dict[encrypted_char_index]

            return encrypted_text
        except Exception as e:
            print(e)

    def index_of_coincidence(self, text):
        n = len(text)
        if n <= 1:
            raise ValueError("Текст слишком короткий для вычисления IC")
        freq = Counter(text)
        IC = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
        return IC


    def find_key_length(self, text, lang, max_key_length=20):
        """
        Находит длину ключа с использованием индекса совпадений.

        :param text: Зашифрованный текст.
        :param max_key_length: Максимальная предполагаемая длина ключа.
        :param lang: Язык текста ('ru' или 'en').
        :return: Список возможных длин ключа.
        """
        standard_ic = self.IC_opentext_ru if lang == 'ru' else self.IC_opentext_en
        _dict = self.ru_dict if lang == 'ru' else self.en_dict
        possible_lengths = []

        for t in range(1, max_key_length + 1):
            # Разделяем текст на t групп
            groups = ['' for _ in range(t)]
            for i, char in enumerate(text):
                groups[i % t] += char

            # Считаем IC для каждой группы
            ic_values = [self.index_of_coincidence(group) for group in groups]

            # Средний IC для текущей длины ключа
            avg_ic = sum(ic_values) / t

            # Если средний IC близок к стандартному, добавляем длину в возможные
            if abs(avg_ic - standard_ic) < 0.01:  # Пороговое значение
                possible_lengths.append((t, avg_ic))

        # Возвращаем список возможных длин ключа, отсортированный по IC
        return sorted(possible_lengths, key=lambda x: -x[1])  # От большего IC к меньшему

    def split_text_by_key_length(self, text, key_length):
        """
        Разбивает текст на группы по длине ключа.
        :param text: Зашифрованный текст.
        :param key_length: Длина ключа.
        :return: Список групп.
        """
        groups = ['' for _ in range(key_length)]
        for i, char in enumerate(text):
            groups[i % key_length] += char
        return groups

    def mutual_index_of_coincidence(self, group_a, group_b, shift, _dict):
        """
        Вычисляет взаимный индекс совпадений (VIC) между двумя строками для заданного сдвига.
        :param group_a: Первая строка.
        :param group_b: Вторая строка.
        :param shift: Сдвиг второй строки.
        :param _dict: Алфавит.
        :return: VIC для текущего сдвига.
        """
        m = len(_dict)
        n_a, n_b = len(group_a), len(group_b)
        shifted_b = ''.join(_dict[(_dict.index(char) - shift) % m] for char in group_b)
        freq_a, freq_b = Counter(group_a), Counter(shifted_b)

        vic = sum(freq_a[char] * freq_b[char] for char in _dict) / (n_a * n_b)
        return vic

    def find_relative_shifts(self, groups, _dict):
        """
        Находит относительные сдвиги между всеми парами групп.
        :param groups: Список групп текста.
        :param _dict: Алфавит.
        :return: Список относительных сдвигов между группами.
        """
        m = len(_dict)
        relative_shifts = []

        for i in range(1):
            for j in range(i + 1, len(groups)):
                max_vic, best_shift = 0, 0
                for s in range(m):
                    vic = self.mutual_index_of_coincidence(groups[i], groups[j], s, _dict)
                    if vic > max_vic:
                        max_vic, best_shift = vic, s

                relative_shifts.append((i, j, (m - best_shift) % m, max_vic))
        # print(relative_shifts)
        return relative_shifts

    def generate_keys(self, shifts, alphabet_size, _dict):
        """
        Генерирует все возможные ключи на основе сдвигов.

        :param shifts: Список относительных сдвигов между строками.
        :param alphabet_size: Размер алфавита (например, 32 для русского или 26 для английского).
        :return: Список всех возможных ключей.
        """
        key_shift = [0]
        for shift in shifts:
            key_shift.append(shift[2])
        keys = []
        for i in range(alphabet_size):
            key = ''
            for item in key_shift:
                key += (_dict[(alphabet_size+i-item)%alphabet_size])
            keys.append(key)
        print(keys)

        return keys

    def friedman_recover_key(self, ciphertext, key_length, language):
        """
        Восстанавливает ключ методом Фридмана.
        :param ciphertext: Зашифрованный текст.
        :param key_length: Длина ключа.
        :param language: Язык текста ('ru' или 'en').
        :return: Восстановленный ключ.
        """
        _dict = self.ru_dict if language == 'ru' else self.en_dict

        # Шаг 1: Разделить текст на группы
        groups = self.split_text_by_key_length(ciphertext, key_length)

        # Шаг 2: Найти относительные сдвиги
        relative_shifts = self.find_relative_shifts(groups, _dict)
        print(relative_shifts)

        # Шаг 3: Построить ключи
        keys = self.generate_keys(relative_shifts, len(_dict), _dict)

        # Шаг 4: Есть все ключи, надо при помощи каждого расшифровать текст и проверить на пригодность и ВСЁ
        key = self.calculate_text_score(ciphertext, keys, language)[0][0]

        return key

    def calculate_text_score(self, text, keys, lang):
        """
        Вычисляет оценку правдоподобности текста на основе частот.

        :param text: Расшифрованный текст.
        :return: Оценка правдоподобности текста.
        """
        language_frequencies = self.freq_ru if lang == 'ru' else self.freq_en
        alphabet = self.ru_dict if lang == 'ru' else self.en_dict
        itog = []
        for key in keys:
            if not self.check_key(key):
                dec_text = self.decrypt_vigenere(text, key, alphabet)
                score = self.calculate_text_score_by_frequencies(dec_text, lang)
                # score = 0
                # total_chars = sum(language_frequencies.values())
                # for char in dec_text:
                #     if char in language_frequencies:
                #         score += language_frequencies[char] / total_chars
                # score = self.index_of_coincidence(text)
                itog.append((key, score))
        itog.sort(key=lambda x: x[1])
        return itog

    def calculate_text_score_by_frequencies(self, text, language):
        """
        Оценивает правдоподобность текста на основе отклонения частот букв.
        :param text: Текст для оценки.
        :param language: Язык текста ('ru' или 'en').
        :return: Оценка текста (чем меньше значение, тем ближе текст к эталонному распределению).
        """
        # Получаем частоты букв из текста
        frequencies = self.get_frequencies(text, language)

        # Эталонные частоты букв
        reference_frequencies = self.freq_ru if language == 'ru' else self.freq_en

        # Вычисляем сумму квадратов разностей частот
        score = sum(
            (frequencies[char] - reference_frequencies.get(char, 0)) ** 2
            for char in frequencies
        )

        return score

    def get_frequencies(self, text, lang):
        """
        Подсчет частот букв в тексте с учетом алфавита.
        """

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


    def decrypt_vigenere(self, text, key, alphabet):
        """
        Расшифровывает текст шифром Виженера.

        :param text: Зашифрованный текст.
        :param key: Ключ (список индексов букв).
        :param alphabet: Список букв алфавита.
        :return: Расшифрованный текст.
        """
        # Определение ключика
        if len(key) < len(text):
            key_line = key * (len(text) // len(key)) + key[:len(text) % len(key)]
        elif len(key) == len(text):
            key_line = key
        else:
            # Тут надо понять, либо ключ сократить, либо ошибку выдать что key > text
            key_line = key[:len(text)]

        # Шифруем
        encrypted_text = ''
        for i in range(len(text)):
            char_index = alphabet.find(text[i])
            key_index = alphabet.find(key_line[i])
            if char_index == -1 or key_index == -1:
                raise Exception(
                    "Шифровальная машина обнаружила ошибку!\nАлгоритм не обнаружил соответсвующий символ в нужном словаре\nСкорее всего ваша оплошность при вводе данных прошла через проверку данных незамеченной!")
            encrypted_char_index = (len(alphabet) + char_index - key_index) % len(alphabet)
            encrypted_text += alphabet[encrypted_char_index]

        return encrypted_text

    # длина ключа совпадает с чем-то там имеет равнок колво единиц и имеет нормальное распределение тогда при шифровании получится четотам шифр
    # если получится 7 бит то гамма тоже меньше -> гамма должна иметь равное кол-во 0 и 1
    def decrypt_text(self, text, lang):
        alphabet = self.ru_dict if lang=='ru' else self.en_dict
        print(sorted(self.find_key_length(text, lang)))
        key_length = sorted(self.find_key_length(text, lang))
        if key_length[0][0] == 1 and key_length[0][1] < key_length[1][1]:
            key_len = key_length[1][0]
        else:
            key_len = key_length[0][0]
        print(key_len)
        # тут ещё надо логику выбора кол-ва знаков ключа доделать,
        # Если ключ - одна буква из алфавита - то это шифр цезаря
        # print(key_length)
        key = self.friedman_recover_key(text, key_len, lang)
        # print(key)
        return self.decrypt_vigenere(text, key, alphabet), key






    def clean_string(self, input_string):
        # Удаляем знаки препинания, но оставляем цифры
        cleaned_string = ''.join(char for char in input_string if char.isalnum() or char.isspace())
        cleaned_string = cleaned_string.replace(" ", "").replace('\n', '').replace('\r', '')
        return cleaned_string.lower()

    def check_alphabeta(self, text, _lang=None):

        ru_range = set(self.ru_dict)
        en_range = set(self.en_dict)
        contains_ru = any(char in ru_range for char in text if char not in '0123456789')
        contains_en = any(char in en_range for char in text if char not in '0123456789')

        if contains_ru and contains_en:
            # print('Тут есть и рус и англ')
            return False

        if _lang is not None:
            if contains_ru and _lang !='ru':
                # print('Тут рус но выбрали en')
                return False
            if contains_en and _lang !='en':
                # print('Тут англ но выбрали ru')
                return False

        return True

    def check_key(self, key):
        return any(char in '0123456789' for char in key)
