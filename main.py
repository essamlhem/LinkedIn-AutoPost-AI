import google.generativeai as genai
import datetime
import os
import requests

# 1. إعداد المفاتيح من Secrets
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_content():
    # تحديد اليوم الحالي
    day_of_week = datetime.datetime.now().weekday()
    
    if day_of_week == 5: # يوم السبت: خطة السلسلة
        prompt = """
        عيسى يريد خطة أسبوعية لسلسلة تقنية على LinkedIn.
        اقترح عنواناً للسلسلة (مثلاً: أسرار مكتبة Pandas أو احتراف Scikit-Learn).
        اعطني عناوين لـ 5 حلقات، واشرح باختصار الكود الذي سنقدمه في كل حلقة.
        خاطب عيسى بحماس.
        """
        prefix = "📅 **خطة الأسبوع الجديد جاهزة يا هندسة:**\n\n"
    
    else: # بقية الأيام: المحتوى التقني + الكود (إلزامي)
        prompt = """
        أنت خبير AI برتبة Senior. اكتب منشوراً لـ LinkedIn كحلقة من سلسلة تعليمية.
        
        **الشروط الإلزامية:**
        1. ابدأ بالعنوان: 🚀 سلسلة تبسيط المفاهيم | حلقة اليوم: [الموضوع].
        2. اشرح المفهوم العلمي بأسطر بسيطة.
        3. **يجب** أن تضع كود Python عملي (Code Snippet) يشرح الفكرة.
        4. اجعل الكود مكتوباً بوضوح (Clean Code).
        5. أضف شرحاً بسيطاً لما يفعله الكود.
        6. انته بسؤال للنقاش مع المتابعين.
        
        **تنبيه:** لا تستخدم تنسيقات Markdown المعقدة، فقط نص واضح وكود برميجي.
        """
        prefix = "🔔 **تذكير النشر اليومي! الحلَقَة مع الكود جاهزة:**\n\n"

    response = model.generate_content(prompt)
    return prefix + response.text

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # إرسال النص كما هو لضمان ظهور الكود بشكل صحيح
    payload = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ تم إرسال الحلقة والكود بنجاح!")
    else:
        print(f"❌ فشل الإرسال: {response.text}")

if __name__ == "__main__":
    try:
        content = get_content()
        send_to_telegram(content)
    except Exception as e:
        print(f"حدث خطأ: {e}")
