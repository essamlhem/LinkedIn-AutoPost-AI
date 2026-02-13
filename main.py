import google.generativeai as genai
from PIL import Image, ImageDraw
import datetime
import os
import requests

# 1. جلب المفاتيح من إعدادات GitHub Secrets
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# إعداد مودل الجيمناي
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_content():
    print("جاري توليد المحتوى عبر Gemini...")
    # تحديد عدد الحروف في البرومبت لتجنب رفض تليجرام للرسالة
    prompt = """
    اكتب منشور LinkedIn تقني احترافي ومبهر بالعربية عن الذكاء الاصطناعي أو تحليل البيانات. 
    المنشور يجب أن يكون:
    - قصير ومركز (أقل من 800 حرف).
    - يحتوي على نصيحة عملية.
    - ينتهي بهاشتاقات مناسبة.
    """
    response = model.generate_content(prompt)
    return response.text

def create_image():
    print("جاري إنشاء صورة البوست...")
    # إنشاء صورة بسيطة (800x400) بخلفية زرقاء داكنة
    img = Image.new('RGB', (800, 400), color=(10, 25, 41))
    # ملاحظة: لإضافة نص عربي داخل الصورة تحتاج لملف خط .ttf في المستودع
    # حالياً سنكتفي بإنشاء الصورة وحفظها
    img_name = "post_image.png"
    img.save(img_name)
    return img_name

def send_to_telegram(text, image_path):
    print("جاري الإرسال إلى تلجرام...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    # تلجرام يسمح بحد أقصى 1024 حرف للوصف المرافق للصورة
    # نقوم بقص النص احتياطياً لضمان عدم حدوث خطأ 400
    safe_caption = text[:1020]
    
    with open(image_path, 'rb') as photo:
        payload = {
            'chat_id': CHAT_ID, 
            'caption': safe_caption,
            'parse_mode': 'Markdown' # اختياري لجعل التنسيق أجمل
        }
        files = {'photo': photo}
        response = requests.post(url, data=payload, files=files)
    
    if response.status_code == 200:
        print("✅ تم الإرسال بنجاح!")
    else:
        print(f"❌ فشل الإرسال. كود الخطأ: {response.status_code}")
        print(f"الرسالة: {response.text}")

# التنفيذ الرئيسي
if __name__ == "__main__":
    try:
        if not all([GEMINI_KEY, TELEGRAM_TOKEN, CHAT_ID]):
            raise ValueError("تأكد من إعداد جميع المفاتيح في GitHub Secrets")
            
        post_text = generate_content()
        image_file = create_image()
        send_to_telegram(post_text, image_file)
        
    except Exception as e:
        print(f"حدث خطأ أثناء التنفيذ: {e}")
