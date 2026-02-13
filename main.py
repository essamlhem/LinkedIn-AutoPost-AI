import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import datetime
import os

# إعداد الجيمناي
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_content():
    prompt = """
    اكتب منشور LinkedIn تقني قصير ومبهر باللغة العربية عن (Data Science أو AI).
    يجب أن يتكون من:
    1. عنوان جذاب وقصير جداً.
    2. محتوى تعليمي بسيط (3 نقاط).
    3. هاشتاقات مناسبة.
    """
    response = model.generate_content(prompt)
    return response.text

def create_image(text_title):
    # إنشاء صورة خلفية زرقاء داكنة (بسيطة واحترافية)
    img = Image.new('RGB', (800, 800), color=(10, 25, 41))
    d = ImageDraw.Draw(img)
    
    # إضافة نص بسيط في المنتصف (يمكنك تطويرها لاحقاً بإضافة لوغو)
    # ملاحظة: لدعم العربية في الصور تحتاج لملف خط يدعم العربية وتمريره هنا
    d.text((100, 350), "Daily Tech Insight", fill=(255, 255, 255))
    d.text((100, 400), text_title[:30] + "...", fill=(0, 255, 150))
    
    img_name = f"post_image_{datetime.date.today()}.png"
    img.save(img_name)
    return img_name

# التشغيل
post_text = generate_content()
# نأخذ أول سطر كعنوان للصورة
title = post_text.split('\n')[0]
image_path = create_image(title)

print(f"✅ تم توليد النص:\n{post_text}")
print(f"✅ تم حفظ الصورة في: {image_path}")
