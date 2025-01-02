from orb_keypoint_descriptors_class import KeypointDescriptor


if __name__ == '__main__':
    orb_keypoint_descriptors = KeypointDescriptor()
    orb_keypoint_descriptors.set_image(image_path='images/my_images/bridge.jpg')
    orb_keypoint_descriptors.get_image(file_path='images/simple_image')
    orb_keypoint_descriptors.get_gray_image(file_path='images/gray_image')
    orb_keypoint_descriptors.get_keypoint_detection(file_path='images/keypoint_detection_image')
    orb_keypoint_descriptors.get_harris_criteria_filtering(file_path="images/filtered_keypoint_detection_image")
    orb_keypoint_descriptors.get_orientation_keypoints(file_path='images/orientation_keypoints_image')
    orb_keypoint_descriptors.get_descriptor(file_path='images/descriptor')
