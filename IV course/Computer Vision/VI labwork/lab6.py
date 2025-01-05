from object_finder_class import ObjectFinder
from orb_keypoint_descriptors_class import KeypointDescriptor
import os


def check_file_in_directory(file_name, directory='./'):
    # Формируем полный путь к файлу
    file_path = os.path.join(directory, file_name)

    # Проверяем, существует ли файл и не пуст ли он
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return True
    else:
        return False


if __name__ == '__main__':
    obj_finder = ObjectFinder()
    obj_finder.set_images(image1_path='images/my_images/box.jpg',
                          image2_path='images/my_images/box_in_scene.jpg')
    obj_finder.get_images(file_path='images/box_and_box_in_scene_image')

    if (not check_file_in_directory(file_name='box_in_scene_keypoints_full_data.json')
            and not check_file_in_directory('box_keypoints_full_data.json')):

        for img in ['images/my_images/box.jpg', 'images/my_images/box_in_scene.jpg']:
            obj_finder.set_image(image_path=img)
            obj_finder.get_image(file_path='images/simple_image')

            if len(obj_finder.image_array.shape) == 3:
                obj_finder.get_gray_image(file_path='images/gray_image')
            elif len(obj_finder.image_array.shape) == 2:
                obj_finder.gray_image_array = obj_finder.image_array
                obj_finder.gray_image = obj_finder.image

            obj_finder.get_descriptor_from_pyramid(filename=img[17:-4])

    box_img_data = obj_finder.load_keypoints_data_from_file('box_keypoints_full_data.json')
    box_in_scene_img_data = obj_finder.load_keypoints_data_from_file('box_in_scene_keypoints_full_data.json')
