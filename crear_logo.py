from PIL import Image, ImageDraw, ImageFont

# Crear una imagen cuadrada blanca
img = Image.new('RGBA', (120, 120), 'white')
draw = ImageDraw.Draw(img)

# Dibujar un círculo azul
draw.ellipse((10, 10, 110, 110), fill='#2196F3', outline='#1565C0', width=4)


# Escribir las iniciales "ALV" (Asesoría Legal Virtual)
try:
    font = ImageFont.truetype('arial.ttf', 36)
except:
    font = ImageFont.load_default()
text = "ALV"
try:
    bbox = font.getbbox(text)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
except Exception:
    w, h = 60, 30  # fallback
draw.text(((120-w)/2, (120-h)/2), text, fill='white', font=font)

img.save('logo.png')
print('Logo generado como logo.png')
