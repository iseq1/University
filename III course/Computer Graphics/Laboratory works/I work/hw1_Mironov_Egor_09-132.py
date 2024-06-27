import math
import numpy as np

# # scalar_product = [] # Список кортежей со скалярными произведениями для каждого ребра грани треугольника
# # скаляры и косинусы пересмотреть!!!!!!!!
# # print(vertex1, vertex2, vertex3)
# # vectors = ((vertex2[0] - vertex1[0], vertex2[1] - vertex1[1], vertex2[2] - vertex1[2]),
# #            (vertex3[0] - vertex2[0], vertex3[1] - vertex2[1], vertex3[2] - vertex2[2]),
# #            (vertex1[0] - vertex3[0], vertex1[1] - vertex3[1], vertex1[2] - vertex3[2]))
# # print(vectors)
# # scalar1 = vectors[0][0] * vectors[1][0] + vectors[0][1] * vectors[1][1] + vectors[0][2] * vectors[1][2]
# # scalar2 = vectors[1][0] * vectors[2][0] + vectors[1][1] * vectors[2][1] + vectors[1][2] * vectors[2][2]
# # scalar3 = vectors[2][0] * vectors[0][0] + vectors[2][1] * vectors[0][1] + vectors[2][2] * vectors[0][2]
# # cos1 = np.round(scalar1/(side1*side2),4)
# # cos2 = np.round(scalar2/(side2*side3),4)
# # cos3 = np.round(scalar3/(side1*side3),4)
# # scalar_product.append((scalar1,scalar2,scalar3))

def load_file(file_path):
    vertices = []  # Список вершин
    faces = []  # Список граней
    with open('teapot.obj', 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(list(map(float, line.split()[1:])))
            elif line.startswith('f '):
                faces.append(list(map(int, line.split()[1:])))
    return np.array(vertices), np.array(faces)

def make_sides(vertex1,vertex2,vertex3):
    side1 = math.sqrt((vertex2[0] - vertex1[0]) ** 2 + (vertex2[1] - vertex1[1]) ** 2 + (vertex2[2] - vertex1[2]) ** 2)
    side2 = math.sqrt((vertex3[0] - vertex2[0]) ** 2 + (vertex3[1] - vertex2[1]) ** 2 + (vertex3[2] - vertex2[2]) ** 2)
    side3 = math.sqrt((vertex1[0] - vertex3[0]) ** 2 + (vertex1[1] - vertex3[1]) ** 2 + (vertex1[2] - vertex3[2]) ** 2)
    return side1, side2, side3

def lengths_n_halfP(vertices, faces):
    edges_lengths = []  # Список длин сторон каждой грани
    halfperimeter = []  # Список полупериметров каждого треугольника
    for face in faces:
        vertex1 = vertices[face[0] - 1]
        vertex2 = vertices[face[1] - 1]
        vertex3 = vertices[face[2] - 1]
        lengths = make_sides(vertex1,vertex2,vertex3)
        halfperimeter.append((lengths[0] + lengths[1] + lengths[2])/2)
        edges_lengths.append(lengths)

    return np.array(edges_lengths), np.array(halfperimeter)


def Square(halfperimeter,edges_lengths ):
    square = []  # Список площадей всех триугольников
    for halfP, lenght in zip(halfperimeter, edges_lengths):
        square.append(math.sqrt(halfP*(halfP-lenght[0])*(halfP-lenght[1])*(halfP-lenght[2])))
    return np.array(square)

def Radius(square, halfperimeter):
    circle_square = []  # Список всех площадей вписанных окружностей
    for S, p in zip(square, halfperimeter):
        r = S/p
        circle_square.append(math.pi*r**2)
    return np.array(circle_square)

def Cosinus(lenght):
    cos = []  # Список кортежей всех косинусов каждого триугольника
    for item in lenght:
        cos1 = (item[1] ** 2 + item[2] ** 2 - item[0] ** 2) / (2 * item[1] * item[2])
        cos2 = (item[0] ** 2 + item[2] ** 2 - item[1] ** 2) / (2 * item[0] * item[2])
        cos3 = (item[0] ** 2 + item[1] ** 2 - item[2] ** 2) / (2 * item[0] * item[1])
        cos.append((cos1, cos2, cos3))
    return np.array(cos)

if __name__ == "__main__":
    vertices, faces = load_file('teapot.obj')
    lenght, p = lengths_n_halfP(vertices, faces)
    S = Square(p, lenght)
    r = Radius(S, p)
    cos = Cosinus(lenght)
    print("\nСуммарная площадь всех вписанных в треугольники окружностей:", np.round(sum(r),4),
          '\nCамый большой косинус угла среди всех треугольников:', np.round(cos.max(),4))
