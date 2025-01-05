from orb_keypoint_descriptors_class import KeypointDescriptor



if __name__ == '__main__':
    orb_keypoint_descriptors = KeypointDescriptor()
    orb_keypoint_descriptors.set_image(image_path='images/my_images/bridge.jpg')
    orb_keypoint_descriptors.get_image(file_path='images/simple_image')

    if len(orb_keypoint_descriptors.image_array.shape) == 3:
        orb_keypoint_descriptors.get_gray_image(file_path='images/gray_image')
    elif len(orb_keypoint_descriptors.image_array.shape) == 2:
        orb_keypoint_descriptors.gray_image_array = orb_keypoint_descriptors.image_array
        orb_keypoint_descriptors.gray_image = orb_keypoint_descriptors.image

    pyramid = orb_keypoint_descriptors.get_descriptor_from_pyramid()

