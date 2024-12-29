from Binary import BinaryCipher
#
# cipher = BinaryCipher()
#
# message = "Тутдлинноесообщениетипатого"
# key = "аш"
# binary_message = cipher.text_to_binary(message)
# binary_key = cipher.text_to_binary(key)
# print(binary_message)
# # print(binary_key)
# IV1 = cipher.generate_gamma(6)
# # print(IV1)
# # тут надо обработать длину ключа па идеи
# IV2 = cipher.xor(binary_key[-6:], IV1)
# # print(IV2)
# c = cipher.split_into_blocks(binary_message)
# # print(c)
# res = cipher.xor_by_blocks(c,IV2)
# # print(res)
# cc = cipher.split_into_blocks(res)
# deres = cipher.xor_by_blocks(cc,IV2)
# print(deres)
# print(cipher.binary_to_text(deres))


cipher = BinaryCipher()

# Ввод данных
message = "itisasimpletextforexample"
key = "key"

# Шифрование
encryption_result = cipher.encrypt(message, key)
print("Бинарный текст:", encryption_result["binary_text"])
print("Бинарный ключ:", encryption_result["binary_key"])
print("IV1:", encryption_result["iv1"])
print("IV2:", encryption_result["iv2"])
print("Зашифрованное сообщение:", encryption_result["encrypted_message"])

# Расшифровка
decrypted_message = cipher.decrypt(encryption_result["encrypted_message"], encryption_result["iv2"])
print("Расшифрованное сообщение:", decrypted_message)
