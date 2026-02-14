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
    أنت خبير تقني تقدم سلسلة تعليمية على LinkedIn بعنوان (سلسلة: "تبسيط المفاهيم" - Simplify Tech).
    مهمتك اليوم هي كتابة "حلقة" احترافية تشرح فيها (مكتبة، تقنية، خوارزمية، أو تابع برمجياً) في مجال الـ AI أو الـ Data Science.
    
    هيكل المنشور المطلوب:
    1. 【العنوان】: ابدأ بـ "🚀 سلسلة تبسيط المفاهيم | حلقة اليوم: [اسم التقنية]".
    2. 【لماذا؟】: اشرح المشكلة التي تحلها هذه التقنية بأسلوب بسيط.
    3. 【في العمق】: اشرح المفهوم العلمي أو طريقة العمل (Mechanism).
    4. 【مثال برميجي】: وضح تابعاً (Function) أو سطر كود مميز لهذه المكتبة.
    5. 【سؤال الحلقة】: سؤال ذكي يحفز المتابعين على النقاش أو اقتراح الحلقة القادمة.
    
    الشروط:
    - الأسلوب: تعليمي رصين ومنظم جداً.
    - اللغة: العربية الفصحى مع المصطلحات الإنجليزية الأساسية.
    - الطول: لا يتجاوز 900 حرف لضمان وصوله للتليجرام.
    - الهاشتاقات: #LearningSeries #DataScience #PythonTips #AI_Education #MachineLearning
    """
    
    response = model.generate_content(prompt)
    return response.text

def send_to_telegram(text):
    print("جاري الإرسال إلى تلجرام...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # تأمين النص لسياسة تلجرام (الحد الأقصى 4096 حرف)
    payload = {
        'chat_id': CHAT_ID, 
        'text': text,
        'parse_mode': 'Markdown' 
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
        # التحقق من وجود الإعدادات
        if not all([GEMINI_KEY, TELEGRAM_TOKEN, CHAT_ID]):
            raise ValueError("نقص في إعدادات GitHub Secrets (Gemini Key, Telegram Token, or Chat ID)")
            
        series_post = generate_series_content()
        send_to_telegram(series_post)
        
    except Exception as e:
        print(f"حدث خطأ أثناء التنفيذ: {e}")
