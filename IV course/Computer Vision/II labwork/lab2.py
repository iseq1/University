from segmentation_class import Segmentation


if __name__ == '__main__':
    segmentation_obj = Segmentation()
    segmentation_obj.set_image(image_path='images/my_images/newyaer.jpg')
    segmentation_obj.get_image(file_path='images/simple_image')
    segmentation_obj.get_gray_image(file_path='images/gray_image')
    segmentation_obj.get_binary_image(file_path='images/binary_image')
    segmentation_obj.get_salt_and_pepper_noise_remover(file_path='images/without_noise_image')
    segmentation_obj.get_seed_growth_segmentation(file_path='images/segmentation_image')
    segmentation_obj.get_color_segments(file_path='images/colored_segmentation_image')
    segmentation_obj.get_histogram(file_path='images/histogram', array=segmentation_obj.gray_image_array)
    segmentation_obj.get_local_minimum_with_neighborhood(file_path='images/histogram_with_local_minimum')
    segmentation_obj.get_seed_growth_segmentation_with_init(file_path='images/seed_growth_segmentation_with_init')
    segmentation_obj.get_colored_image_new(file_path='images/colored_image_new')

