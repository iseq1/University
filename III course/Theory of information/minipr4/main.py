import os

#Алгоритм LZW

def read_file(file_path):
    # Чтение данных из исходного файла
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    dictionary = {}
    index = 0
    for word in data.split(' '):
        if word not in dictionary:
            dictionary[word] = index
            index += 1

    return data, dictionary, os.path.getsize(file_path)

def compress_data(data, dictionary):
    # Архивация данных
    compressed_file = "compressed.bin"
    compressed_data = [dictionary[word] for word in data.split(' ')]
    with open(compressed_file, 'wb') as writer:
        for code in compressed_data:
            writer.write(code.to_bytes(4, byteorder='little'))
    print('Сжатые данные архивированы в', compressed_file)

    return os.path.getsize(compressed_file)


def decompress_data(dictionary, compress_file_path, decompress_file_path):
    decompressed_data = []
    with open(compress_file_path, 'rb') as reader:
        while True:
            code_bytes = reader.read(4)
            if not code_bytes:
                break
            code = int.from_bytes(code_bytes, byteorder='little')
            for entry, value in dictionary.items():
                if value == code:
                    decompressed_data.append(entry + " ")
                    break
    # Сохранение распакованных данных
    with open(decompress_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(decompressed_data))
    print('Расжатые данные разархивированы в', decompress_file_path)

    return os.path.getsize(decompress_file_path)



data, dict, size = read_file('LostLetter.txt')
compress_size = compress_data(data, dict)
decompress_size = decompress_data(dict,'compressed.bin', 'decompressed.txt')


print("\nРазмер исходного файла:", size / 1024, "Кбайт")
print("Размер сжатого файла словарным алгоритмом:", compress_size / 1024, "Кбайт")
print("Размер расжатого файла словарным алгоритмом:", decompress_size / 1024, "Кбайт")