import math
import string
from PIL import Image
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator)
    return cleaned_text
def remove_spaces_and_newlines(text):
    text = text.replace('\n', '').replace('\t', '').replace(' ', '')
    text = ''.join(text.split())
    return text
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return remove_spaces_and_newlines(remove_punctuation(text))
def count_characters(text):
    char_count = {}
    total_characters = len(text)

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    probabilities = {}
    for char, count in char_count.items():
        probabilities[char] = "{:.10f}".format(count/total_characters)

    return char_count, probabilities
def character_entropy(character_probabilities):
    entropy = 0
    for char, probability in character_probabilities.items():
        probability = float(probability)
        entropy += (probability*(math.log2(1/probability)))
    return entropy
def read_img_from_file(file_path):
    # Загрузка изображения и преобразование в черно-белое
    image = Image.open(file_path)
    bw_image = image.convert("L")
    # image.show()
    # bw_image.show()
    return bw_image
def count_pixels(image):
    # Получение гистограммы интенсивностей пикселей
    pixel_counts = image.histogram()
    # Вычисление общего количества пикселей
    total_pixels = image.width * image.height
    return pixel_counts, total_pixels
def pixels_entropy(probabilities):
    entropy = -sum(p * math.log2(p) if p != 0 else 0 for p in probabilities)
    return entropy

# (a)
file_path_txt = 'Похищенное письмо Эдгар Алан По.txt'
text = read_text_from_file(file_path_txt)
# (b)
character_count, character_probabilities = count_characters(text)
# print("\n===============================")
# print("Количество появлений каждого символа:")
# for char, count in character_count.items():
#     print(f"Символ '{char}': {count}")
# print("\n===============================")
# print("\nВероятность каждого символа:")
# for char, probability in character_probabilities.items():
#     print(f"Символ '{char}': {probability}")
# (c)
H_character = character_entropy(character_probabilities)
# (d)
entropy_of_book = H_character*len(text)
print(f"Энтропия символа: {round(H_character,2)}")
print(f"Общая энтропия текста: {round(entropy_of_book, 2)}")

# (e)
file_path_img = 'Похищенное письмо.jpg'
image = read_img_from_file(file_path_img)
# (f)
pixel_counts, total_pixels = count_pixels(image)
probabilities = [count / total_pixels for count in pixel_counts]
# # Вывод количества пикселей для каждой интенсивности
# print("Количество пикселей для каждой интенсивности:")
# for intensity, count in enumerate(pixel_counts):
#     print(f"Интенсивность {intensity}: {count} пикселей")
# (g)
H_pixel = pixels_entropy(probabilities)
# (h)
total_entropy = H_pixel * total_pixels
print(f"Энтропия пикселя: {round(H_pixel,2)}")
print(f"Общая энтропия рисунка: {round(total_entropy, 2)}")


