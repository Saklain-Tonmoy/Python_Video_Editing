import os
from PIL import Image
from datetime import datetime


class ImageResizer:

    def __init__(self):
        # Folder which contains all the images
        self.images_path = f"{os.getcwd()}/images/"
        self.resized_images_path = f"{os.getcwd()}/resized_images/"

    def resize_image(self):
        print("#######################################\n")
        print("          Resizing Images          ")
        print("#######################################\n")
        start_time = datetime.now().replace(microsecond=0)
        print(f"Start Time: {str(start_time)}")

        # resized_images_path = f"{os.getcwd()}/resized_images/"
        if not os.path.exists(self.resized_images_path):
            os.mkdir(self.resized_images_path)


        # Resizing of the images to give
        # them same width and height
        for file in os.listdir(self.images_path):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                # opening image using PIL Image
                im = Image.open(os.path.join(self.images_path, file))

                # im.size includes the height and width of image
                # width, height = im.size
                # print(width, height)

                # resizing
                imResize = im.resize((3000, 1600), Image.ANTIALIAS)
                imResize.save(f"{self.resized_images_path}{file}", 'JPEG', quality=95)

        end_time = datetime.now().replace(microsecond=0)
        execution_time = (end_time - start_time)
        print(f"End Time: {str(end_time)}")
        print(f"Execution Time: {str(execution_time)}")
