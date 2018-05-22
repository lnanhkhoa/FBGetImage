
import os
import requests
from PIL import Image, ImageFont, ImageDraw, ImageOps
from config import DATABASE_CONFIG


class ProcessImage:
    def __init__(self, stored_image_path, stored_all_images_path):
        self.stored_image_path = stored_image_path
        self.stored_all_images_path = stored_all_images_path
        self.path_image = DATABASE_CONFIG['path_image']
        self.tree_path = DATABASE_CONFIG['tree_path']

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

    def add_likes_shares_into_image(self, name, like_share):
        file = './{0}/{1}/{2}'.format(self.path_image, self.tree_path, name)
        read_image = Image.open(file)
        font_type = ImageFont.truetype("./apps/asserts/fonts/FreeMono.ttf", 40, encoding="unica")
        read_image_with_border = ImageOps.expand(read_image, border=50, fill='black')
        draw = ImageDraw.Draw(read_image_with_border)
        width, h = read_image.size
        draw.text(xy=(width / 4, 10), text=like_share, fill=(255, 255, 255), font=font_type)
        read_image_with_border.save(file)

        file = './{0}/{1}/{2}'.format(self.path_image, 'all', name)
        read_image = Image.open(file)
        font_type = ImageFont.truetype("./apps/asserts/fonts/FreeMono.ttf", 40, encoding="unica")
        read_image_with_border = ImageOps.expand(read_image, border=50, fill='black')
        draw = ImageDraw.Draw(read_image_with_border)
        width, h = read_image.size
        draw.text(xy=(width / 4, 10), text=like_share, fill=(255, 255, 255), font=font_type)
        read_image_with_border.save(file)
