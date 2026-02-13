import google.generativeai as genai
from PIL import Image, ImageDraw
import datetime
import os
import requests

# 1. التحقق من وجود المفاتيح (للتصحيح فقط)
print("--- Checking Environment Variables ---")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"Gemini Key loaded: {bool(GEMINI_KEY)}")
print(f"Telegram Token loaded: {bool(TELEGRAM_TOKEN)}")
print(f"Chat ID loaded: {bool(CHAT_ID)}")

if not all([GEMINI_KEY, TELEGRAM_TOKEN, CHAT_ID]):
    print("❌ Error: One or more environment variables are missing!")
    exit(1)

# 2. إعداد الجيمناي
try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("--- Gemini Configured ---")
except Exception as e:
    print(f"❌ Gemini Config Error: {e}")

def generate_content():
    print("Generating content...")
    prompt = "اكتب منشور LinkedIn تقني احترافي ومبهر بالعربية عن الذكاء الاصطناعي أو تحليل البيانات."
    response = model.generate_content(prompt)
    print("Content generated successfully.")
    return response.text

def create_image():
    print("Creating image...")
    img = Image.new('RGB', (800, 400), color=(10, 25, 41))
    img_name = "post_image.png"
    img.save(img_name)
    print(f"Image saved as {img_name}")
    return img_name

def send_to_telegram(text, image_path):
    print("Sending to Telegram...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as photo:
        payload = {'chat_id': CHAT_ID, 'caption': text}
        files = {'photo': photo}
        response = requests.post(url, data=payload, files=files)
    
    print(f"Telegram Response Status: {response.status_code}")
    print(f"Telegram Response Text: {response.text}")

# التنفيذ
try:
    txt = generate_content()
    img = create_image()
    send_to_telegram(txt, img)
    print("--- PROCESS COMPLETED ---")
except Exception as e:
    print(f"❌ Execution Error: {e}")
