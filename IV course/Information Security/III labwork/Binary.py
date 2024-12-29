import random
class BinaryCipher:
    def __init__(self, bit_size=6):
        self.alphabet = (
            "абвгдежзийклмнопрстуфхцчшщъыьэюя"
            "abcdefghijklmnopqrstuvwxyz"
        )
        self.bit_size = bit_size  # Фиксированная длина двоичного кода

    def char_to_binary(self, char):
        char = char.lower()
        index = self.alphabet.index(char)
        return f'{index:0{self.bit_size}b}'

    def text_to_binary(self, text):
        return ''.join(self.char_to_binary(char) for char in text if char.lower() in self.alphabet)

    def binary_to_text(self, binary):
        chars = [binary[i:i+self.bit_size] for i in range(0, len(binary), self.bit_size)]
        return ''.join(self.alphabet[int(char, 2)] for char in chars)

    def xor_with_key(self, binary_text, binary_key):
        # Удлиняем ключ до длины текста
        repeated_key = (binary_key * (len(binary_text) // len(binary_key) + 1))[:len(binary_text)]
        # Применяем XOR
        encrypted_binary = self.xor(binary_text, repeated_key)
        return encrypted_binary

    def xor(self, a, b):
        """
        Выполняет побитовый XOR двух строк одинаковой длины.
        """
        return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

    def split_into_blocks(self, binary_text, block_size=6):
        """
        Разделяет бинарный текст на блоки фиксированной длины.
        Если длина текста не кратна block_size, дополняет последний блок нулями.
        """
        # Дополняем текст нулями, чтобы длина была кратна block_size
        if len(binary_text) % block_size != 0:
            padding_length = block_size - (len(binary_text) % block_size)
            binary_text += '0' * padding_length

        blocks = [binary_text[i:i + block_size] for i in range(0, len(binary_text), block_size)]

        return blocks

    def xor_by_blocks(self, blocks, iv2):
        """
        Шифрует бинарное сообщение в режиме CBC.
        """
        encrypted_blocks = []
        previous_result = None
        for i, block in enumerate(blocks):
            if i == 0:
                # Первый блок XOR'ится с IV2
                current_result = self.xor(block, iv2)
            else:
                # Каждый следующий блок XOR'ится с результатом предыдущего
                current_result = self.xor(block, previous_result)
            encrypted_blocks.append(current_result)
            previous_result = current_result  # Сохраняем результат для следующего блока
        return {
            "iv2": iv2,
            "encrypted_message": ''.join(encrypted_blocks),
            "encrypted_blocks": encrypted_blocks
        }

    def encrypt(self, text, key):
        """
        Полный процесс шифрования текста.
        """
        # Перевод текста и ключа в бинарный вид
        binary_text = self.text_to_binary(text)
        binary_key = self.text_to_binary(key)

        # Генерация начального итерационного вектора
        iv1 = self.generate_gamma(self.bit_size)
        iv2 = self.xor(iv1, binary_key[-6:])

        # Разделение текста на блоки
        blocks = self.split_into_blocks(binary_text, block_size=self.bit_size)

        # Шифрование по блокам
        encryption_result = self.xor_by_blocks(blocks, iv2)

        return {
            "binary_text": binary_text,
            "binary_key": binary_key,
            "iv1": iv1,
            "iv2": encryption_result["iv2"],
            "encrypted_message": encryption_result["encrypted_message"],
            "encrypted_blocks": encryption_result["encrypted_blocks"]
        }

    def decrypt(self, encrypted_message, iv2):
        """
        Полный процесс расшифровки сообщения.
        """
        # Разделение зашифрованного сообщения на блоки
        blocks = self.split_into_blocks(encrypted_message, block_size=self.bit_size)

        # Расшифровка по блокам
        decrypted_blocks = []
        previous_result = None

        for i, block in enumerate(blocks):
            if i == 0:
                # Первый блок расшифровывается с использованием IV2
                decrypted_block = self.xor(block, iv2)
            else:
                # Каждый последующий блок расшифровывается с использованием предыдущего блока
                decrypted_block = self.xor(block, previous_result)
            decrypted_blocks.append(decrypted_block)
            previous_result = block  # Текущий зашифрованный блок становится предыдущим

        # Объединяем все блоки и возвращаем исходный текст
        binary_message = ''.join(decrypted_blocks)
        return self.binary_to_text(binary_message), binary_message

    def generate_gamma(self, binary_length):
        """
        Генерирует гамму заданной длины с равным количеством 0 и 1 (или почти равным при нечётной длине).
        """
        # Если длина нечётная, добавляем 1 бит (0 или 1) для чётности
        if binary_length % 2 != 0:
            binary_length += 1  # Делаем длину чётной

        # Половина бит — нули, половина — единицы
        half_length = binary_length // 2
        gamma_bits = [0] * half_length + [1] * half_length  # Формируем список из половины 0 и половины 1

        # Перемешиваем биты случайным образом
        random.shuffle(gamma_bits)

        # Преобразуем список битов в строку
        return ''.join(map(str, gamma_bits))


    def clean_string(self, input_string):
        # Удаляем знаки препинания, но оставляем цифры
        cleaned_string = ''.join(char for char in input_string if char.isalnum() or char.isspace())
        cleaned_string = cleaned_string.replace(" ", "").replace('\n', '').replace('\r', '')
        return cleaned_string.lower()

    def check_alphabeta(self, text, _lang=None):

        ru_range = set('абвгдежзийклмнопрстуфхцчшщъыьэюя')
        en_range = set('abcdefghijklmnopqrstuvwxyz')
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