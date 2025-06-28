from PIL import Image

width, height = 512, 512

img = Image.new("RGB", (width, height))

for y in range(height):

    ratio = y / (height - 1)

    r = int(255 * ratio)
    g = int(255 * ratio)
    b = int(255 * ratio + (1 - ratio) * 255)  
    
    for x in range(width):
        img.putpixel((x, y), (r, g, b))

img.save("smooth_gradient.bmp")
