import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


def get_screen_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width

def load_obj(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                # Считываем только первые два значения (x и y)
                x, y = map(float, line.split()[1:3])
                vertices.append([x, y])
            elif line.startswith('f '):
                faces.append(list(map(int, line.split()[1:])))
    return np.array(vertices), np.array(faces)

def scale_matrix(sx,sy):
    return np.array([[sx,0,0],
                     [0,sy,0],
                     [0,0,1]])

def translation_matrix(tx,ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])

def scale_and_translate(vertices, image_size):
    coef = image_size / 3 / 3
    scale = scale_matrix(coef, coef)
    translation = translation_matrix(image_size // 2, image_size // 2)
    transformation = np.dot(translation, scale)
    scaled_vertices = []
    for item in vertices:
        point = np.array([item[0], item[1], 1])
        transformed_point = np.dot(transformation, point)
        scaled_vertices.append([transformed_point[0], transformed_point[1]])

    return scaled_vertices

def draw_line(image, x0, y0, x1, y1, color):
    x0, x1, y0, y1 = map(int, [x0, x1, y0, y1])
    dx, dy = map(abs, [x1-x0, y1-y0])
    dy = -dy
    epsilon = dx+dy

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    while True:
        image[y0, x0, :] = color
        if (x0, y0) == (x1, y1):
            break
        if 2 * epsilon >= dy:
            if x0 == x1:
                break
            epsilon += dy
            x0 += sx
        if 2 * epsilon <= dx:
            if y0 == y1:
                break
            epsilon += dx
            y0 += sy


# Создание изображения с градиентным фоном и отображение граней модели
def draw_model(vertices, faces, image_size):
    image = np.zeros((image_size, image_size, 3), dtype=np.uint8)
    scaled_vertices = scale_and_translate(vertices, image_size)

    gradient = np.linspace(0, 255, image_size)
    background = np.zeros((image_size, image_size, 3))
    background[:, :, 0] = 255  # Красный канал
    background[:, :, 1] = gradient  # Зеленый канал

    for face in faces:
        for i in range(3):
            vertex1 = scaled_vertices[face[i] - 1]
            vertex2 = scaled_vertices[face[(i + 1) % 3] - 1]

            x1, y1 = int(vertex1[0]), int(vertex1[1])
            x2, y2 = int(vertex2[0]), int(vertex2[1])

            if (0 <= x1 < image_size and 0 <= y1 < image_size
            and 0 <= x2 < image_size and 0 <= y2 < image_size):
                draw_line(image, x1, y1, x2, y2, background[y1, x1])

    return image


def save_image(image, file_path):
    plt.ylim(image_size, 0)
    plt.gca().invert_yaxis()
    plt.imshow(image)
    plt.savefig(file_path)
    plt.show()

if __name__ == "__main__":
    image_size = int(get_screen_size()/3)
    vertices, faces = load_obj('teapot.obj')
    image = draw_model(vertices, faces, image_size)
    output_file = 'output.png'
    save_image(image, output_file)


