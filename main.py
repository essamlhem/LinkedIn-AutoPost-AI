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
    print("جاري توليد محتوى علمي عالي القيمة...")
    prompt = """
    أنت خبير في علوم البيانات والذكاء الاصطناعي وهدفك بناء مجتمع تعليمي على LinkedIn.
    اكتب منشوراً باللغة العربية يركز على تقديم "قيمة علمية" حقيقية.
    
    هيكل المنشور:
    1. 【خطاف/Hook】: جملة قوية عن تحدي تقني أو معلومة صادمة في الـ AI.
    2. 【المحتوى العلمي】: شرح مفهوم تقني واحد بعمق (مثلاً: Data Leakage, Overfitting, Feature Engineering, أو Transformer Models).
    3. 【نصيحة عملية】: كيف يمكن للمهندسين تطبيق هذا المفهوم في مشاريعهم؟
    4. 【سؤال تفاعلي】: سؤال يفتح باب النقاش (مثلاً: "كيف تتعاملون مع هذه المشكلة في بيئة العمل؟").
    5. 【دعوة للتعلم】: ترشيح مصطلح تقني للقراء للبحث عنه.

    الشروط:
    - اللغة: عربية فصحى بسيطة مع المصطلحات التقنية بالإنجليزية.
    - الطول: كحد أقصى 950 حرف لضمان وصوله للتليجرام.
    - الهاشتاقات: #DataScience #AI #MachineLearning #ContinuousLearning #Python
    """
    response = model.generate_content(prompt)
    return response.text

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
