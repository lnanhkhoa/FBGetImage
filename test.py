
from PIL import Image, ImageFont, ImageOps, ImageDraw
like_share="like share"
file = '../33072615_2491716734187502_5570887129136889856_n.jpg'
read_image = Image.open(file)
font_type = ImageFont.truetype("./apps/asserts/fonts/FreeMono.ttf", 40, encoding="unica")
read_image_with_border = ImageOps.expand(read_image, border=50, fill='black')
draw = ImageDraw.Draw(read_image_with_border)
w, h = read_image.size
#draw.rectangle(((0, 0), (200, 200)), fill="black", outline="blue")
padding = [30, 10]
draw.text(xy=(w/2 - padding[0], padding[1]), text=like_share, fill=(255, 255, 255), font=font_type)
read_image_with_border.save(file)
