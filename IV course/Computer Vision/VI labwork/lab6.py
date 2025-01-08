from object_finder_class import ObjectFinder
import os

if __name__ == '__main__':
    obj_finder = ObjectFinder()
    obj_finder.set_images(image1_path='images/my_images/box.jpg',
                          image2_path='images/my_images/box_in_scene.jpg')
    obj_finder.get_images(file_path='images/box_and_box_in_scene_image')
    obj_finder.image1_array = obj_finder.scale(obj_finder.image1_array, 2)

    matrix = obj_finder.get_hamming_matrix()
    print("Матрица расстояний Хэмминга:\n", matrix, '\n')

    lower_test_result = obj_finder.get_lower_test()
    print(f"Количество удовлетворяющих Lower test точек\n\tна 1-ом изо: {len(lower_test_result[0])}\n\tна 2-ом изo: {len(lower_test_result[1])}\n")
    # print(f"Удовлетворяющие точки: {lower_test_result}")

    cross_test_result = obj_finder.get_cross_test()
    print(f"Количество удовлетворяющих Cross test точек\n\tна 1-ом изо: {len(cross_test_result[0])}\n\tна 2-ом изo: {len(cross_test_result[1])}\n")
    # print(f"Удовлетворяющие точки: {cross_test_result}")

    obj_finder.get_visualize_matches(file_path="images/keypoints_matches")

    M, T = obj_finder.RANSAC(cross_test_result[0], cross_test_result[1], 5, 2)
    obj_finder.get_detected_img(M, T, file_path="images/detected_image")
