
from RSA import generate_rsa_keys, rsa_encrypt, rsa_decrypt
import threading
import time
from server import Server
from client import Client

def run_server():
    Server('localhost', 12345, 1024).start_server()

def run_client():
    Client('localhost', 12345, 1024).start_client()

if __name__ == "__main__":
    # это надо чтобы клиент и сервер начали свою работу одновременно
    server_thread = threading.Thread(target=run_server)
    client_thread = threading.Thread(target=run_client)

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()





