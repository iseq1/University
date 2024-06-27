import socket
from RSA import rsa_encrypt


class Client:
    """
    Представляет клиента, который подключается к серверу.

    Атрибуты:
    host (str): имя хоста или IP-адрес, который будет использоваться клиентом.
    port (int): порт, который будет использоваться клиентом.
    """
    def __init__(self, host, port, bit_length):
        self.host = host
        self.port = port
        self.bit_length = bit_length

    def start_client(self, message="Я, Миронов Егор Петрович, шифрую сообщение для преподавателя, Еникеева Разиля Радиковича!!!"):
        """
        Запускает клиент и осуществляет связь с сервером.

        Этот метод подключается к серверу, используя указанный хост и порт.
        Запрашивает открытый ключ с сервера, шифрует сообщение с помощью RSA,
        и отправляет зашифрованное сообщение на сервер.

        Зашифрованное сообщение отправляется с использованием сокетного соединения.

        Returns:
        None
        """
        with socket.socket() as sock:
            # конект с сервером по хосту и порту
            sock.connect((self.host, self.port))
            print(f"Клиент подключен к серверу {self.host}:{self.port}")

            # Получение открытого ключа от сервера
            e_bytes = sock.recv(128)
            n_bytes = sock.recv(256)
            e = int.from_bytes(e_bytes, byteorder='big')
            n = int.from_bytes(n_bytes, byteorder='big')
            public_key = (e, n)

            # Шифрование сообщения
            # принимает сообщение, открытый ключ и размер блока для шифрования, а затем шифрует сообщение с помощью алгоритма RSA
            encrypted_message = rsa_encrypt(message, public_key, 2 * self.bit_length)

            # Отправка зашифрованного сообщения серверу
            sock.send(encrypted_message)
            print(f"Зашифрованное сообщение отправлено серверу")




