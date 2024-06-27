from HuffmanNode import Huffman

h = Huffman("LostLetter.txt")
output_path = h.compress()
decom_path = h.decompress(output_path)
print("Кодировка символов: " + str(h.codes))
print("Сжатый файл: " + output_path)
print("Разжатый файл: " + decom_path)

