from PIL import Image, ImageDraw, ImageFont

# Create a blank white image
img = Image.new('RGB', (600, 400), color='white')
draw = ImageDraw.Draw(img)

# Load handwriting font
font = ImageFont.truetype("PatrickHand-Regular.ttf", 28)

# Sample table lines
lines = [
    "Number    Name               Quantity",
    "006       Dennis Alpha       195",
    "007       Carol Beta        300",
    "008       Samuel Gamma       121",
    "009       Jane Delta    221",
    "010       Peter Epsilon     90",
    "011       Amos Zeta          510"
]

y_text = 20
for line in lines:
    draw.text((20, y_text), line, fill='black', font=font)
    y_text += 45

img.save("sample_table_handwritten_2.jpg")
print("✅ Handwriting-style image saved!")
