
import os
import requests
from PIL import Image, ImageFont, ImageDraw, ImageOps

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
            read_image = Image.open(handle)
            font_type = ImageFont.truetype("./asserts/fonts/FreeMono.ttf", 40, encoding="unica")
            read_image_with_border = ImageOps.expand(read_image, border=200, fill='black')
            draw = ImageDraw.Draw(read_image_with_border)
            #draw.rectangle(((0, 0), (200, 200)), fill="black", outline="blue")
            draw.text(xy=(400, 150), text=number_of_likes+' '+'likes'+' '+number_of_shares, fill=(255, 255, 255), font=font_type)
            read_image_with_border.save(file)

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
