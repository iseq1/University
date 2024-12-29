import random


class Hamming:

    def __init__(self, block_len=8):
        """
        Инициализирует объект с заданной длиной блока и вычисляет биты проверки

        :param block_len: Длина блока, используемая для кодирования (по умолчанию 8).
                          Должна быть положительным целым числом.
        """
        self.BLOCK_LENGTH = self.check_chunk_length(block_len)
        self.CHECK_BITS = [i for i in range(1, block_len + 1) if not i & (i - 1)]

    @staticmethod
    def check_chunk_length(chunk_length: int) -> int:
        """
        Проверка задаваемой длины блока, которая должна быть кратна 8.

        :param chunk_length: Длина блока
        :return: Длина блока, если она кратна 8
        :raises ValueError: если длина блока не кратна 8
        """
        if chunk_length % 8 == 0:
            return chunk_length
        else:
            raise ValueError("Длина блока должна быть кратна 8")

    def chars_to_bin(self, chars: str) -> str:
        """
        Преобразует строку символов в бинарное представление.

        :param chars: Строка символов для преобразования
        :return: Бинарная строка, представляющая символы
        :raises ValueError: если длина кодируемых данных не кратна длине блока кодирования
        """
        if len(chars) * 8 % self.BLOCK_LENGTH != 0:
            raise ValueError("Длина кодируемых данных должна быть кратна длине блока кодирования")
        else:
            return ''.join([bin(ord(char))[2:].zfill(8) for char in chars])

    @staticmethod
    def block_iterator(text_bin: str, chunk_size: int) -> str:
        """
        Генератор, который разбивает бинарный текст на блоки фиксированной длины.

        :param chunk_size: Длина каждого блока.
        :param text_bin: Бинарная строка
        :return: Бинарная подстрока определенной длины
        """
        for i in range(len(text_bin)):
            if not i % chunk_size:
                yield text_bin[i:i + chunk_size]

    def set_empty_check_bits(self, block_bin: str) -> str:
        """
        Добавляет в бинарный блок "пустые" контрольные биты

        :param block_bin: Бинарная строка заданной длины
        :return: Обновленная бинарная строка со значением "0" в местах контрольных бит
        """
        for bit in self.CHECK_BITS:
            block_bin = block_bin[:bit - 1] + '0' + block_bin[bit - 1:]
        return block_bin

    @staticmethod
    def decompose_into_powers_of_two(n: int) -> list:
        """
        Раскладывает входящее число n на слагаемые по степеням двойки

        :param n: Число для разложения
        :return: Список, содержащий степени числа два, которые в сумме дают n
        """
        powers = []
        power = 0
        while (1 << power) <= n:  # Используем битовый сдвиг для получения степеней двойки
            if n & (1 << power):
                powers.append(1 << power)
            power += 1
        return powers

    def get_check_bits_data(self, block_bin: str) -> dict:
        """
        Получение информации о контрольных битах из бинарного блока данных

        :param block_bin: Строка, представляющая двоичный блок, где каждый символ соответствует биту (0 или 1).
        :return: Словарь, где ключи - это степени двойки (бит-коды проверки), а значения - количество единиц,
        найденных в соответствующих местах двоичного блока
        """
        check_bits_count_map = {k: 0 for k in self.CHECK_BITS}
        for i in range(len(block_bin)):
            for item in self.decompose_into_powers_of_two(i + 1):
                check_bits_count_map[item] += int(block_bin[i])
        return check_bits_count_map

    def set_check_bits(self, block_bin: str) -> str:
        """
        Устанавливает биты проверки для заданного двоичного блока

        :param block_bin: Строка, представляющая двоичный блок, где каждый символ соответствует биту (0 или 1),
        без битов проверки.
        :return: Строка, представляющая двоичный блок с установленными битами проверки.
        """
        block_bin = self.set_empty_check_bits(block_bin)
        check_bits_data = self.get_check_bits_data(block_bin)
        for check_bit, bit_value in check_bits_data.items():
            block_bin = '{0}{1}{2}'.format(block_bin[:check_bit - 1], bit_value % 2, block_bin[check_bit:])
        return block_bin

    def encode(self, text: str) -> str:
        """
        Кодирует текст в двоичную строку с добавлением битов проверки.

        :param text: Исходный текст для кодирования
        :return: Двоичная строка, полученная после кодирования исходного текста с установленными битами проверки.
        """
        text_bin = self.chars_to_bin(text)
        result = ''
        for block in self.block_iterator(text_bin, self.BLOCK_LENGTH):
            block = self.set_check_bits(block)
            result += block
        return result

    def get_check_bits(self, encoded_block: str) -> dict:
        """
        Извлекает контрольные биты из закодированного блока

        :param encoded_block: Закодированный блок данных, представленный в виде строки
        :return: Словарь, где ключами являются индексы битов проверки, а значениями - соответствующие биты
         из закодированного блока
        """
        check_bits = {}
        for index, value in enumerate(encoded_block, 1):
            if index in self.CHECK_BITS:
                check_bits[index] = int(value)
        return check_bits

    def exclude_check_bits(self, value_bin: str) -> str:
        """
        Исключает информацию о контрольных битах из блока бинарных данных

        :param value_bin: Закодированный блок данных
        :return: Блок данных без участия контрольных битов
        """
        clean_value_bin = ''
        for index, char_bin in enumerate(list(value_bin), 1):
            if index not in self.CHECK_BITS:
                clean_value_bin += char_bin

        return clean_value_bin

    @staticmethod
    def fix_error(encoded_block: str, check_bits_encoded: dict, check_bits: dict) -> str:
        """
        Исправляет ошибку в закодированном блоке, основываясь на контрольных битах.

        :param encoded_block: Закодированный блок данных, где требуется исправление
        :param check_bits_encoded: Словарь, содержащий закодированные контрольные биты и их значения
        :param check_bits: Словарь, содержащий фактические значения контрольных битов
        :return: Исправленный закодированный блок данных в виде строки
        """
        invalid_bits = []
        for check_bit_encoded, value in check_bits_encoded.items():
            if check_bits[check_bit_encoded] != value:
                invalid_bits.append(check_bit_encoded)
        num_bit = sum(invalid_bits)
        encoded_block = '{0}{1}{2}'.format(
            encoded_block[:num_bit - 1],
            int(encoded_block[num_bit - 1]) ^ 1,
            encoded_block[num_bit:])
        return encoded_block

    def check_and_fix_error(self, encoded_block: str) -> str:
        """
        Проверяет закодированный блок на наличие ошибок и при необходимости исправляет его

        :param encoded_block: Закодированный блок данных, который необходимо проверить и исправить
        :return: Исправленный закодированный блок данных в виде строки, если ошибка была исправлена,
        иначе возвращает оригинальный закодированный блок
        """
        check_bits_encoded = self.get_check_bits(encoded_block)
        check_block = self.exclude_check_bits(encoded_block)
        check_block = self.set_check_bits(check_block)
        check_bits = self.get_check_bits(check_block)
        if check_bits_encoded != check_bits:
            return self.fix_error(encoded_block, check_bits_encoded, check_bits)
        return encoded_block

    def decode(self, encoded_text: str, fix_error: bool = True) -> str:
        """
        Декодирует закодированный текст, исправляя возможную ошибки

        :param encoded_text: Закодированный текст в виде бинарных данных
        :param fix_error: Флаг, указывающий, нужно ли исправлять ошибки в закодированном тексте. По умолчанию True
        :return: Декодированный текст как строка
        """
        decoded_text = ''
        fixed_encoded_list = []
        for encoded_block in self.block_iterator(encoded_text, self.BLOCK_LENGTH + len(self.CHECK_BITS)):
            if fix_error:
                encoded_block = self.check_and_fix_error(encoded_block)
            fixed_encoded_list.append(encoded_block)

        clean_block_list = []
        for encoded_block in fixed_encoded_list:
            encoded_block = self.exclude_check_bits(encoded_block)
            clean_block_list.append(encoded_block)

        for clean_block in clean_block_list:
            for clean_char in [clean_block[i:i + 8] for i in range(len(clean_block)) if not i % 8]:
                decoded_text += chr(int(clean_char, 2))
        return decoded_text

    def set_errors(self, encoded):
        """
        Допустить ошибку в блоках бинарных данных

        :param encoded: Закодированные бинарные данные, в которых необходимо допустить ошибку
        :return: Закодированные бинарные данные с внесенной ошибкой
        """
        result = ''
        for block in self.block_iterator(encoded, self.BLOCK_LENGTH + len(self.CHECK_BITS)):
            num_bit = random.randint(1, len(block))
            block = '{0}{1}{2}'.format(block[:num_bit - 1], int(block[num_bit - 1]) ^ 1, block[num_bit:])
            result += block

        return result

    @staticmethod
    def get_diff_index_list(value_bin1: str, value_bin2: str) -> list:
        """
        Находит индексы символов, которые различаются в двух бинарных строках

        :param value_bin1: Первая бинарная строка
        :param value_bin2: Вторая бинарная строка
        :return: Список индексов, по которым бинарные строки различаются
        """
        diff_index_list = []
        for index, char_bin_items in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
            if char_bin_items[0] != char_bin_items[1]:
                diff_index_list.append(index)
        return diff_index_list
