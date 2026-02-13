import google.generativeai as genai
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

def generate_scientific_content():
    print("جاري توليد محتوى علمي عالي القيمة...")
    
    prompt = """
    أنت خبير في علوم البيانات والذكاء الاصطناعي وهدفك بناء مجتمع تعليمي احترافي على LinkedIn.
    اكتب منشوراً باللغة العربية يركز على تقديم "قيمة علمية" حقيقية.
    
    هيكل المنشور المطلوب:
    1. 【العنوان】: جملة خاطفة عن تحدي تقني أو حقيقة في الـ AI.
    2. 【الشرح العلمي】: شرح مفهوم تقني عميق بتبسيط (مثل: Gradient Descent, Data Leakage, Backpropagation, or Model Tuning).
    3. 【الفائدة العملية】: كيف يستفيد المهندس أو المحلل من هذا المفهوم في شغله؟
    4. 【سؤال النقاش】: سؤال تقني ذكي يحفز الخبراء على التعليق ومشاركة تجاربهم.
    
    الشروط:
    - اللغة: عربية رصينة مع مصطلحات تقنية بالإنجليزية.
    - الطول: كحد أقصى 900 حرف لضمان وصوله للتليجرام كاملاً.
    - الهاشتاقات: #DataScience #ArtificialIntelligence #MachineLearning #TechEducation
    """
    
    response = model.generate_content(prompt)
    return response.text

def send_to_telegram(text):
    print("جاري الإرسال إلى تلجرام...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # تأمين طول النص لسياسة تلجرام
    safe_text = text[:4000] # sendMessage يدعم حتى 4096 حرف
    
    payload = {
        'chat_id': CHAT_ID, 
        'text': safe_text,
        'parse_mode': 'Markdown' 
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ تم إرسال المحتوى العلمي بنجاح!")
    else:
        print(f"❌ فشل الإرسال. كود الخطأ: {response.status_code}")
        print(f"الرسالة: {response.text}")

# التنفيذ الرئيسي
if __name__ == "__main__":
    try:
        if not all([GEMINI_KEY, TELEGRAM_TOKEN, CHAT_ID]):
            raise ValueError("نقص في مفاتيح الإعدادات (Secrets)")
            
        scientific_post = generate_scientific_content()
        send_to_telegram(scientific_post)
        
    except Exception as e:
        print(f"حدث خطأ: {e}")
