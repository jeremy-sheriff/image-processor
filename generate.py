from PIL import Image, ImageDraw, ImageFont

# Create a blank white image
img = Image.new('RGB', (600, 400), color='white')
draw = ImageDraw.Draw(img)

# Load handwriting font
font = ImageFont.truetype("PatrickHand-Regular.ttf", 28)

# Sample table lines
lines = [
    "Number    Name               Quantity",
    "001       Widget Alpha       15",
    "002       Gadget Beta        30",
    "003       Device Gamma       12",
    "004       Component Delta    22",
    "005       Module Epsilon     9",
    "006       Part Zeta          50"
]

y_text = 20
for line in lines:
    draw.text((20, y_text), line, fill='black', font=font)
    y_text += 45

img.save("sample_table_handwritten.jpg")
print("✅ Handwriting-style image saved!")
