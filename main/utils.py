import random
import string
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont

def generate_captcha_text(length=6):
    """Генерирует случайную строку из букв и цифр для капчи."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_captcha_image(text):
    """Генерирует PNG-капчу и возвращает base64-строку."""
    width, height = 140, 48
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # Можно указать свой путь к ttf-файлу, если нужен другой шрифт
    try:
        font = ImageFont.truetype('arial.ttf', 32)
    except Exception:
        font = ImageFont.load_default()
    # Рисуем текст с шумом
    for i in range(random.randint(1, 3)):
        draw.line(
            [(random.randint(0, width), random.randint(0, height)),
              (random.randint(0, width), random.randint(0, height))],
            fill=(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)), width=2)
    draw.text((16, 8), text, font=font, fill=(random.randint(0, 100), 0, 0))
    # Добавляем точки-шум
    for _ in range(30):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=(random.randint(0,255),0,0))
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str 