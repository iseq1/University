import socket
from RSA import generate_rsa_keys, rsa_decrypt


class Server:
    """
    Класс, представляющий сервер, использующий шифрование RSA для безопасной связи.

    Атрибуты:
    host (str): адрес хоста, на котором работает сервер.
    port (int): номер порта, который прослушивает сервер.
    bit_length (int): длина в битах, используемая для ключей шифрования RSA.
    """

    def __init__(self, host, port, bit_length):
        self.host = host
        self.port = port
        self.bit_length = bit_length

    # Создание сервера
    def start_server(self):
        """
        Запускает сервер, прослушивает входящие соединения и обрабатывает шифрование RSA для безопасной связи.

        Returns:
        None
        """
        with socket.socket() as sock:
            # связь сокета с указанными хостом и портом
            sock.bind((self.host, self.port))
            # ожидаем подключения к серверному сокету
            sock.listen(1)
            print(f"Сервер запущен и слушает порт {self.port}")
            # получаем входящее соединение - кортеж с новым сокетом для обмена данными и адресом клиента
            conn, addr = sock.accept()
            print(f"Подключен клиент с адресом {addr}")

            with conn:
                # Генерация ключей RSA
                public_key, private_key = generate_rsa_keys(self.bit_length)
                e, n = public_key

                # Отправка открытого ключа клиенту
                conn.send(e.to_bytes((e.bit_length() + 7) // 8, byteorder='big'))
                conn.send(n.to_bytes((n.bit_length() + 7) // 8, byteorder='big'))

                # Получение зашифрованного сообщения от клиента
                encrypted_message = conn.recv(4096)

        # Расшифровка сообщения
        decrypted_message = rsa_decrypt(encrypted_message, private_key, 2 * self.bit_length)
        print(f"Расшифрованное сообщение: {decrypted_message}")

