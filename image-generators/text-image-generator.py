from PIL import Image, ImageDraw, ImageFont
import textwrap

img = Image.new('L', (512, 512), color=255)
draw = ImageDraw.Draw(img)

tekst = (
"The universe is the vast expanse of space and time that encompasses all matter, energy, planets, stars, galaxies, and even the emptiness between them. It is unimaginably large and represents one of the greatest mysteries humanity has ever sought to understand. Since the earliest days of civilization, humans have looked up at the starry sky with awe and wonder, asking questions about what lies beyond. They have pondered how the cosmos began and whether there is something even farther than what the eye can see. Current scientific understanding suggests that the universe began approximately thirteen point eight billion years ago in an event known as the Big Bang. At that moment, all space, time, matter, and energy were compressed into a singular point of infinite density and temperature. Suddenly, this point began to expand rapidly, creating space and time as we know them today. Since then, the universe has continued to expand, cooling down and allowing the formation of the first particles, atoms, stars, galaxies, and eventually the complex structures we observe now. The structure of the universe is not uniform. On a grand scale, it consists of immense voids, or empty spaces, with galaxies and galaxy clusters scattered throughout. Galaxies are enormous systems containing billions or even hundreds of billions of stars, along with planets, gas, dust, and mysterious dark matter. Our own galaxy, the Milky Way, holds between one hundred and four hundred billion stars, including our sun and its surrounding planets."
)

try:
    font = ImageFont.truetype("arial.ttf", 14)
except IOError:
    font = ImageFont.load_default()

lines = textwrap.wrap(tekst, width=70)
y_text = 20

for line in lines:
    bbox = draw.textbbox((0, 0), line, font=font)
    text_width = bbox[2] - bbox[0]
    x_text = (512 - text_width) // 2
    draw.text((x_text, y_text), line, font=font, fill=0)
    y_text += 18  

img.save("text.bmp")
print("Image successfuly generated: text.bmp")
