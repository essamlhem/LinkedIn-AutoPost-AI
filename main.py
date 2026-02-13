import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import datetime
import os
import requests

# إعدادات المفاتيح (سنجلبها من GitHub Secrets لاحقاً للأمان)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_content():
    prompt = "اكتب منشور LinkedIn تقني احترافي ومبهر بالعربية عن الذكاء الاصطناعي أو تحليل البيانات. اجعله بأسلوب شيق مع هاشتاقات."
    response = model.generate_content(prompt)
    return response.text

def create_image(text_title):
    img = Image.new('RGB', (800, 400), color=(10, 25, 41))
    d = ImageDraw.Draw(img)
    # ملاحظة: للنصوص العربية في الصور نحتاج ملف خط .ttf، حالياً سنكتب بالإنجليزية للتبسيط
    d.text((50, 150), "New Tech Insight Today!", fill=(255, 255, 255))
    img_name = "post_image.png"
    img.save(img_name)
    return img_name

def send_to_telegram(text, image_path):
    # إرسال الصورة مع النص كـ Caption
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        payload = {'chat_id': CHAT_ID, 'caption': text}
        files = {'photo': photo}
        requests.post(url, data=payload, files=files)

# التشغيل
post_text = generate_content()
image_path = create_image("AI Insight")
send_to_telegram(post_text, image_path)

print("🚀 تم إرسال البوست والصورة إلى تلجرام بنجاح!")
