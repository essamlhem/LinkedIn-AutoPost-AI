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
    # معرفة اليوم (0: الاثنين, 5: السبت, 6: الأحد)
    day_of_week = datetime.datetime.now().weekday()
    
    if day_of_week == 5: # يوم السبت: خطة السلسلة
        prompt = """
        اقترح عنواناً لسلسلة تعليمية تقنية للأسبوع القادم (مثلاً في الـ AI أو Data Science).
        ثم اعطني عناوين لـ 5 حلقات، كل حلقة يجب أن تحتوي على فكرة برمجية قوية.
        تحدث مع عيسى بلهجة تشجيعية.
        """
        prefix = "📅 **عيسى، هذي خطة السلسلة الجديدة للأسبوع الجاي:**\n\n"
    
    else: # باقي الأيام: المحتوى التقني مع الكود
        prompt = """
        أنت خبير في الـ AI و Python. اكتب منشوراً احترافياً لـ LinkedIn كجزء من سلسلة تعليمية.
        المتطلبات:
        1. ابدأ بعنوان الحلقة (مثلاً: الحلقة رقم 3: أسرار الـ List Comprehension).
        2. اشرح معلومة تقنية دسمة بأسلوب بسيط.
        3. ضغ كود بايثون (Python Code) عملي وقصير يشرح الفكرة (تأكد أن الكود نظيف ومنظم).
        4. انتهِ بسؤال يحفز المتابعين على تجربة الكود أو النقاش.
        5. لا تستخدم رموز Markdown معقدة (مثل النجوم الكثيرة) لتجنب أخطاء التليجرام.
        """
        prefix = "🔔 **تذكير النشر اليومي! حلقة السلسلة جاهزة يا هندسة:**\n\n"

    response = model.generate_content(prompt)
    return prefix + response.text

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # إرسال الرسالة كنص عادي لتجنب أخطاء الرموز في الكود البرمجي
    payload = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("✅ تم الإرسال.")
    else:
        print(f"❌ خطأ: {response.text}")

if __name__ == "__main__":
    try:
        content = get_content()
        send_to_telegram(content)
    except Exception as e:
        print(f"حدث خطأ: {e}")
