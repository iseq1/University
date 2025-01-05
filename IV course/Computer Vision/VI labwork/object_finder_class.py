from orb_keypoint_descriptors_class import *


class ObjectFinder(KeypointDescriptor):
    def __init__(self):
        super().__init__()
        self.image1, self.image2 = None, None
        self.image1_array, self.image2_array = None, None
        self.image1_gray, self.image2_gray = None, None
        self.image1_gray_array, self.image2_gray_array = None, None

    def set_images(self, image1_path, image2_path):
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        self.image1 = image1
        self.image2 = image2
        self.image1_array = np.array(image1)
        self.image2_array = np.array(image2)

    def get_images(self, file_path):
        '''
        Показываю оригинальную картинку
        :return:
        '''
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("box")
        plt.imshow(self.image1, cmap='gray')

        plt.subplot(1, 2, 2)
        plt.title("box_in_scene")
        plt.imshow(self.image2, cmap='gray')
        plt.savefig(f'{file_path}', bbox_inches='tight')
        plt.show()

