
import os
import requests


class ProcessImage:

    def __init__(self, stored_image_path, stored_all_images_path):
        self.stored_image_path = stored_image_path
        self.stored_all_images_path = stored_all_images_path

    def get_image_from_url(self, pic_url, name):
        file = os.path.join(self.stored_image_path, name)
        with open(file, 'wb') as handle:
            response = requests.get(pic_url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def get_image_into_all(self, pic_url, name):
        file = os.path.join(self.stored_all_images_path, name)
        with open(file, 'wb') as handle:
            response = requests.get(pic_url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
