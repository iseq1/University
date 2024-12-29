from edge_detector_class import EdgeDetector

if __name__ == '__main__':
    edge_detector = EdgeDetector()
    edge_detector.set_image(image_path='images/my_images/hoodie (1).jpg')
    edge_detector.get_image(file_path='images/simple_image')
    edge_detector.get_gray_image(file_path='images/gray_image')
    edge_detector.get_blured_image(file_path='images/blured_image')
    edge_detector.get_gradient_n_magnitude(file_path=[
        'images/gradient_by_x_image',
        'images/gradient_by_y_image',
        'images/gradient_magnitude_image',
        'images/gradient_direction_image',
    ])
    edge_detector.get_gradient_direction_round(file_path='images/gradient_direction_round_image')
    edge_detector.get_non_maximum_suppression(file_path='images/non_maximum_suppression_image')
    edge_detector.get_hysteresis_thresholding(file_path=[
        'images/hysteresis_thresholding_image',
        'images/new_old_image',
    ])

