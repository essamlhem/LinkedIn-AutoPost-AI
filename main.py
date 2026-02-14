import google.generativeai as genai
import datetime
import os
import requests

# 1. إعداد المفاتيح من GitHub Secrets
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 2. إعداد مودل الجيمناي
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_series_content():
    print("جاري توليد حلقة من السلسلة التعليمية...")
    
    prompt = """
    أنت خبير تقني تقدم سلسلة تعليمية على LinkedIn بعنوان (سلسلة: "تبسيط المفاهيم").
    اكتب حلقة تشرح فيها (مكتبة، تقنية، أو خوارزمية) في مجال الـ AI.
    
    شروط هامة للنص:
    - لا تستخدم الرموز البرمجية المعقدة مثل الأقواس المتداخلة بكثرة.
    - اجعل النص بسيطاً ومنظماً.
    - ابدأ بـ: 🚀 سلسلة تبسيط المفاهيم | حلقة اليوم: [اسم الموضوع].
    - اذكر الفائدة، الشرح، ومثال كود بسيط جداً.
    - الطول الإجمالي أقل من 900 حرف.
    """
    
    response = model.generate_content(prompt)
    return response.text

def send_to_telegram(text):
    print("جاري الإرسال إلى تلجرام...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # قمنا بإزالة parse_mode لضمان عدم حدوث خطأ في الرموز
    payload = {
        'chat_id': CHAT_ID, 
        'text': text
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ تم إرسال الحلقة بنجاح!")
    else:
        print(f"❌ فشل الإرسال. كود الخطأ: {response.status_code}")
        print(f"الرسالة: {response.text}")

# 3. التنفيذ الرئيسي
if __name__ == "__main__":
    try:
        if not all([GEMINI_KEY, TELEGRAM_TOKEN, CHAT_ID]):
            raise ValueError("نقص في إعدادات Secrets")
            
        series_post = generate_series_content()
        send_to_telegram(series_post)
        
    except Exception as e:
        print(f"حدث خطأ: {e}")
