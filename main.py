import google.generativeai as genai
import datetime
import os
import requests

# 1. إعداد المفاتيح
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_content():
    day_of_week = datetime.datetime.now().weekday()
    
    if day_of_week == 5: # السبت: خطة الأسبوع
        prompt = "عيسى يريد خطة أسبوعية لسلسلة تقنية (AI/Python) على LinkedIn. اقترح 5 مواضيع دسمة مع لمحة عن الكود الذي ستقدمه في كل حلقة."
        prefix = "📅 **خطة السلسلة الجديدة يا هندسة:**\n\n"
    else: # باقي الأيام: المحتوى التقني + الكود
        prompt = """
        اكتب حلقة احترافية لسلسلة تقنية على LinkedIn. 
        يجب أن يتضمن المنشور:
        1. شرح لمفهوم تقني (مثل: Decorators, Generators, Lambda functions, or AI Layers).
        2. **كود بايثون (Python Code) كامل وعملي يشرح المفهوم.**
        3. شرح بسيط لما يقوم به الكود.
        4. سؤال تفاعلي للجمهور.
        
        مهم جداً: اجعل النص مختصراً لضمان وصوله للتليجرام (أقل من 2000 حرف).
        """
        prefix = "🔔 **تذكير: وقت النشر! حلقة اليوم مع الكود جاهزة:**\n\n"

    response = model.generate_content(prompt)
    return prefix + response.text

def send_to_telegram(text):
    print("جاري الإرسال...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # الحل النهائي لمشكلة الـ Parsing: نرسل النص كـ Plain Text بدون Markdown
    # لضمان وصول الكود والرموز (مثل _ و *) بدون أخطاء
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ تم الإرسال بنجاح!")
    else:
        # إذا فشل بسبب الطول، نحاول قص النص وإرساله
        print(f"⚠️ فشل الإرسال الأول، جاري محاولة إرسال نص مختصر...")
        payload['text'] = text[:4000] 
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ تم الإرسال (نسخة مختصرة).")
        else:
            print(f"❌ خطأ نهائي: {response.text}")

if __name__ == "__main__":
    try:
        content = get_content()
        send_to_telegram(content)
    except Exception as e:
        print(f"حدث خطأ: {e}")
