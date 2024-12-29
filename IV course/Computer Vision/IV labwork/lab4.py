from hough_transform_class import HoughTransform


if __name__ == '__main__':
    hough_transform = HoughTransform()
    hough_transform.set_image(image_path='images/my_images/Screenshot_2.jpg')
    hough_transform.get_image(file_path='images/simple_image')
    hough_transform.get_gray_image(file_path='images/gray_image')
    hough_transform.get_blured_image(file_path='images/blured_image')
    hough_transform.get_gradient_n_magnitude(file_path=[
        'images/gradient_by_x_image',
        'images/gradient_by_y_image',
        'images/gradient_magnitude_image',
        'images/gradient_direction_image',
    ])
    hough_transform.get_gradient_direction_round(file_path='images/gradient_direction_round_image')
    hough_transform.get_non_maximum_suppression(file_path='images/non_maximum_suppression_image')
    hough_transform.get_hysteresis_thresholding(file_path=[
        'images/hysteresis_thresholding_image',
        'images/new_old_image',
    ])
    hough_transform.get_hough_transform(file_path='images/hough_transform')
    hough_transform.get_hough_transform_smoothed(file_path='images/hough_transform_smoothed')
    hough_transform.get_non_maximum_suppression_haff(file_path='images/non_maximum_suppression_haff')
    hough_transform.get_draw_lines_on_image(file_path='images/image_with_lines')


