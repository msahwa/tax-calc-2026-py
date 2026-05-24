import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

# 1. إعدادات الصفحة البرمجية لواجهة التطبيق
st.set_page_config(
    page_title="حاسبة الضرائب المصرية الذكية 2025",
    page_icon="🇪🇬",
    layout="centered"
)

# عنوان التطبيق ومقدمة بسيطة
st.title("🇪🇬 حاسبة ضريبة الدخل المصرية الذكية لعام 2025")
st.write("أدخل صافي الربح السنوي ليقوم الذكاء الاصطناعي بتقسيم الشرائح وحساب الضريبة المستحقة فوراً.")

# 2. إدخال مفتاح الـ API بأمان من خلال الشريط الجانبي (Sidebar)
st.sidebar.header("🔐 إعدادات الاتصال")
API_KEY = st.sidebar.text_input("أدخل مفتاح Gemini API Key الخاص بك:", type="password")

if not API_KEY:
    st.info("💡 يرجى إدخال مفتاح Gemini API الخاص بك في الشريط الجانبي لتفعيل الحاسبة ذكياً.", icon="🔑")
else:
    # تهيئة مكتبة جوجل وتحديد إصدار الـ API (v1beta) في خيارات العميل لتفادي خطأ الـ 404 والـ Unknown field
    opts = client_options.ClientOptions(api_version="v1beta")
    genai.configure(api_key=API_KEY, client_options=opts)
    
    # 3. توجيهات النظام (System Instructions) الموجهة لـ Gemini
    system_instruction = """
    You are an expert Egyptian Tax Calculator Application. Your sole task is to calculate the personal income tax for the year 2025 based on the Egyptian Tax Law (Law 91 of 2005 and its latest amendments up to 2025/2026).

    When the user enters a number representing the "Net Profit" (صافي الربح السنوي), apply the following progressive tax brackets strictly:
    1. From 1 to 40,000 EGP: 0%
    2. From 40,001 to 55,000 EGP: 10%
    3. From 55,001 to 70,000 EGP: 15%
    4. From 70,001 to 200,000 EGP: 20%
    5. From 200,001 to 400,000 EGP: 22.5%
    6. From 400,001 to 1,200,000 EGP: 25%
    7. Above 1,200,000 EGP: 27.5%

    Output Requirements (Strictly in Arabic):
    - Provide a clear, concise breakdown of the calculation per bracket.
    - State the Total Tax Due (إجمالي الضريبة المستحقة).
    - State the Net Profit After Tax (صافي الربح بعد الضريبة).
    - Keep the tone professional, direct, and accounting-focused. No conversational fluff.

    Example Output format:
    - الوعاء الخاضع للضريبة: [X] جنيه
    - تفصيل حساب الشرائح: [Detail]
    - إجمالي الضريبة المستحقة: [Y] جنيه
    - صافي الربح بعد الضريبة: [Z] جنيه
    """

    # 4. واجهة المستخدم لادخال البيانات
    net_profit = st.number_input("صافي الربح السنوي الخاضع للضريبة (بالجنيه):", min_value=0.0, step=1000.0, format="%.2f")
    
    if st.button("احسب الضريبة المستحقة"):
        if net_profit == 0:
            st.warning("يرجى إدخال مبلغ أكبر من الصفر للحساب.")
        else:
            with st.spinner("جاري معالجة الوعاء وتفنيد الشرائح ضريبياً..."):
                try:
                    # استخدام الاسم الرسمي للموديل مع تمرير التعليمات
                    model = genai.GenerativeModel(
                        model_name="models/gemini-1.5-flash", 
                        system_instruction=system_instruction
                    )
                    
                    # إرسال قيمة صافي الربح بشكل مباشر ونظيف
                    response = model.generate_content(f"صافي الربح السنوي هو: {net_profit}")
                    
                    # عرض النتيجة والتقرير الضريبي
                    st.success("تم احتساب الضريبة بنجاح!")
                    st.markdown("### 📊 التقرير الضريبي التفصيلي:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالخادم: {e}")

st.caption("تم تطوير هذه الأداة كحل محاسبي ذكي بالاعتماد على بايثون ونماذج Gemini.")
