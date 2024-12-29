from computer_vision_class import Computer_Vision

def actual_work_way(image_path):
    computer_vision_obj = Computer_Vision()
    computer_vision_obj.set_image(f'{image_path}')
    computer_vision_obj.get_image(file_path='images/simple_image')
    computer_vision_obj.get_inverted_image(file_path='images/inverted_image')
    computer_vision_obj.get_gray_image(file_path='images/gray_image')
    computer_vision_obj.get_noisy_image(file_path='images/noisy_image')
    computer_vision_obj.get_histogram(file_path='images/histogram')
    computer_vision_obj.get_blured_image(file_path='images/blurred_image')
    computer_vision_obj.get_equalized_histogram(file_path='images/equalized_histogram')
    computer_vision_obj.get_equalized_image(file_path='images/equalized_image')


if __name__ == '__main__':
    actual_work_way('images/my_images/temp.jpg')

