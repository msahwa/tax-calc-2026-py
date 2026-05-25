import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية لتشبه المواقع الاحترافية
st.set_page_config(
    page_title="منظومة التخطيط والحسابات الضريبية المصرية",
    page_icon="📊",
    layout="wide", # استخدام كامل عرض الشاشة مثل موقع أسماء
    initial_sidebar_state="expanded"
)

# تطبيق تنسيقات CSS مخصصة لجعل الخطوط والألوان متناسقة وعصرية وترتيب الاتجاه من اليمين لليسار (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .stNumberInput label, .stSelectbox label {
        font-weight: 600 !important;
        color: #1e293b !important;
        font-size: 14px !important;
    }
    .metric-card {
        background-color: #f8fafc;
        border-right: 5px solid #0284c7;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 14px;
        color: #64748b;
        font-weight: bold;
    }
    .metric-value {
        font-size: 22px;
        color: #0f172a;
        font-weight: 700;
        margin-top: 5px;
    }
    .tax-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. تصميم الشريط الجانبي (Sidebar) والمخيّرات المتطابقة مع الأدوات الضريبية
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=80)
st.sidebar.markdown("### 🏛️ المنظومة الضريبية الذكية")
st.sidebar.markdown("---")

# قائمة الخيارات بالشريط الجانبي للتنقل بين التطبيقات والخدمات الضريبية المختلفة
app_mode = st.sidebar.radio(
    "اختر الأداة الضريبية الحسابية:",
    [
        "🧮 حساب ضريبة الأرباح التجارية والصناعية",
        "💼 حساب ضريبة المرتبات (كسب العمل)",
        "🏢 حساب وعاء الأشخاص الاعتبارية (الشركات)",
        "📊 جدول المقارنة الضريبية للشرائح"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**مكتب المحاسبة والاستشارات الضريبية**
أدوات رقمية متطورة لتسهيل الفحص والتخطيط الضريبي وفقاً لأحدث القوانين المصرية لعام 2025.
""")

# دالة حسابية صارمة لحساب الضريبة التصاعدية للأشخاص الطبيعيين (تعديلات 2025 السارية)
def calculate_natural_tax(net_income):
    # تعريف الشرائح ونسبها وحدودها القصوى والدنيا
    brackets = [
        (40000, 0.00),   # الشريحة الأولى: معفاة حتى 40,000
        (15000, 0.10),   # الشريحة الثانية: من 40,000 إلى 55,000
        (15000, 0.15),   # الشريحة الثالثة: من 55,000 إلى 70,000
        (130000, 0.20),  # الشريحة الرابعة: من 70,000 إلى 200,000
        (200000, 0.225), # الشريحة الخامسة: من 200,000 إلى 400,000
        (800000, 0.25),  # الشريحة السادسة: من 400,000 إلى 1,200,000
        (float('inf'), 0.275) # الشريحة السابعة: ما زاد عن 1,200,000
    ]
    
    tax_due = 0.0
    remaining = net_income
    breakdown = []
    
    for i, (limit, rate) in enumerate(brackets):
        if remaining <= 0:
            break
        
        # تحديد الجزء الخاضع للضريبة في هذه الشريحة
        taxable_in_bracket = min(remaining, limit)
        bracket_tax = taxable_in_bracket * rate
        tax_due += bracket_tax
        remaining -= taxable_in_bracket
        
        if taxable_in_bracket > 0:
            breakdown.append({
                "الشريحة": f"الشريحة {i+1} ({int(rate*100)}%)",
                "المبلغ الخاضع": f"{taxable_in_bracket:,.2f} ج.م",
                "الضريبة المستحقة": f"{bracket_tax:,.2f} ج.م"
            })
            
    return tax_due, breakdown

# --- 3. تشغيل صفحات التطبيق بناءً على اختيار الشريط الجانبي ---

if app_mode == "🧮 حساب ضريبة الأرباح التجارية والصناعية":
    st.markdown('<div class="tax-header"><h2>حاسبة ضريبة الأرباح التجارية والصناعية والمهنية (2025)</h2><p>حساب دقيق لضريبة الأشخاص الطبيعيين وتفنيد تفصيلي لكافة الشرائح القانونية.</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📥 مدخلات الوعاء السنوي")
        annual_profit = st.number_input("صافي الربح السنوي الخاضع للضريبة (ج.م):", min_value=0.0, value=150000.0, step=5000.0, format="%.2f")
        st.caption("أدخل صافي الربح السنوي الإجمالي بعد خصم كافة التكاليف والمصروفات واجبة الخصم قانوناً.")
        
    with col2:
        st.subheader("📊 ناتج الفحص والحساب الضريبي")
        
        # إجراء الحسبة الرياضية الفورية
        total_tax, tax_table = calculate_natural_tax(annual_profit)
        net_after_tax = annual_profit - total_tax
        effective_rate = (total_tax / annual_profit * 100) if annual_profit > 0 else 0.0
        
        # عرض النتائج في بطاقات منظمة مثل موقع أسماء
        c_res1, c_res2, c_res3 = st.columns(3)
        with c_res1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">إجمالي الضريبة المستحقة</div><div class="metric-value" style="color:#dc2626;">{total_tax:,.2f} ج.م</div></div>', unsafe_allow_html=True)
        with c_res2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">صافي الربح بعد الضريبة</div><div class="metric-value" style="color:#16a34a;">{net_after_tax:,.2f} ج.م</div></div>', unsafe_allow_html=True)
        with c_res3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">العـبء الضريبي الفعلي</div><div class="metric-value">{effective_rate:.2f} %</div></div>', unsafe_allow_html=True)
            
        st.write("#### 📑 تفنيد احتساب الشرائح التصاعدية:")
        if tax_table:
            df_tax = pd.DataFrame(tax_table)
            st.table(df_tax)
        else:
            st.info("الوعاء المدخل يقع بالكامل ضمن الشريحة المعفاة.")

elif app_mode == "💼 حساب ضريبة المرتبات (كسب العمل)":
    st.markdown('<div class="tax-header"><h2>حاسبة ضريبة كسب العمل (المرتبات وما في حكمها)</h2><p>حساب ضريبة المرتبات مع إدراج حد الإعفاء الشخصي للموظفين.</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        gross_monthly = st.number_input("إجمالي الأجر الشهري (ج.م):", min_value=0.0, value=12000.0, step=500.0)
        insurance_deduction = st.number_input("الاستقطاعات الشهريّة (تأمينات اجتماعية) (ج.م):", min_value=0.0, value=1300.0)
        
        # الإعفاء الشخصي للمرتبات لعام 2025 (20,000 جنيه سنوياً)
        personal_exemption_annual = 20000.0
        
    with col2:
        # تحويل الأرقام إلى سنوي لحساب الوعاء الخاضع بدقة
        annual_taxable_salary = ((gross_monthly - insurance_deduction) * 12) - personal_exemption_annual
        
        if annual_taxable_salary < 0:
            annual_taxable_salary = 0.0
            
        total_tax_annual, tax_table_salary = calculate_natural_tax(annual_taxable_salary)
        monthly_tax = total_tax_annual / 12
        
        st.subheader("📋 نتيجة احتساب كسب العمل الشهري")
        
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">الضريبة الاستقطاعية الشهرية</div><div class="metric-value" style="color:#dc2626;">{monthly_tax:,.2f} ج.م</div></div>', unsafe_allow_html=True)
        with c_m2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">صافي الأجر الشهري المقبوض</div><div class="metric-value" style="color:#16a34a;">{(gross_monthly - insurance_deduction - monthly_tax):,.2f} ج.م</div></div>', unsafe_allow_html=True)
            
        st.write(f"**الوعاء السنوي الخاضع للضريبة بعد خصم الإعفاء الشخصي:** {annual_taxable_salary:,.2f} ج.م")
        if tax_table_salary:
            st.table(pd.DataFrame(tax_table_salary))

elif app_mode == "🏢 حساب وعاء الأشخاص الاعتبارية (الشركات)":
    st.markdown('<div class="tax-header"><h2>حاسبة ضريبة الأشخاص الاعتبارية (الشركات والجمعيات)</h2><p>حساب الضريبة المفروضة على أرباح شركات الأموال وشركات الأشخاص (السعر القطعي).</p></div>', unsafe_allow_html=True)
    
    company_profit = st.number_input("صافي الأرباح السنوية المعدلة للمنشأة الاعتبارية (ج.م):", min_value=0.0, value=1000000.0, step=50000.0)
    
    # السعر العام لضريبة الشركات في مصر هو 22.5% (باستثناء الجهات الخاصة مثل قناة السويس والبترول وهي 40%)
    tax_rate_corp = 0.225
    corp_tax_due = company_profit * tax_rate_corp
    
    c_c1, c_c2 = st.columns(2)
    with c_c1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">سعر الضريبة على الشركات (سعر قطعي)</div><div class="metric-value">22.5 %</div></div>', unsafe_allow_html=True)
    with c_c2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">إجمالي الضريبة المستحقة على الشركة</div><div class="metric-value" style="color:#dc2626;">{corp_tax_due:,.2f} ج.م</div></div>', unsafe_allow_html=True)

elif app_mode == "📊 جدول المقارنة الضريبية للشرائح":
    st.markdown('<div class="tax-header"><h2>الدليل التعريفي لشرائح مصلحة الضرائب المصرية لعام 2025</h2><p>جدول استرشادي يوضح كيفية تصاعد نسب الضرائب تدرجاً مع زيادة حجم الوعاء السنوي.</p></div>', unsafe_allow_html=True)
    
    brackets_data = {
        "الشريحة": [f"الشريحة {i}" for i in range(1, 8)],
        "المدى السنوي للمبلغ (ج.م)": [
            "من 1 إلى 40,000",
            "من 40,001 إلى 55,000",
            "من 55,001 إلى 70,000",
            "من 70,001 إلى 200,000",
            "من 200,001 إلى 400,000",
            "من 400,001 إلى 1,200,000",
            "ما زاد عن 1,200,000"
        ],
        "نسبة الضريبة المفروضة": ["0% (معفاة تماماً)", "10%", "15%", "20%", "22.5%", "25%", "27.5%"]
    }
    st.table(pd.DataFrame(brackets_data))
