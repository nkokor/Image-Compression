from PIL import Image, ImageDraw
import random

width, height = 512, 512

img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

for _ in range(20):
    shape_type = random.choice(['rectangle', 'ellipse'])
    x1, y1 = random.randint(0, width-100), random.randint(0, height-100)
    x2, y2 = x1 + random.randint(30, 150), y1 + random.randint(30, 150)
    color = random_color()

    if shape_type == 'rectangle':
        draw.rectangle([x1, y1, x2, y2], fill=color, outline="black")
    else:
        draw.ellipse([x1, y1, x2, y2], fill=color, outline="black")

img.save("geometric-shapes.bmp")
