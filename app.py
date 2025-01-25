import streamlit as st
import pandas as pd  # لإنشاء الجداول

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# حالة اللغة (العربية أو الإنجليزية)
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# اختيار اللغة في السايد بار
language = st.sidebar.selectbox("اختر اللغة / Choose Language", ["العربية", "English"])

# الأسعار المبدئية
if "egg_price" not in st.session_state:
    st.session_state.egg_price = 0.1155
if "feed_price" not in st.session_state:
    st.session_state.feed_price = 0.0189

# تغيير اتجاه الكتابة بناءً على اللغة
if language == "العربية":
    st.markdown(
        f"""
        <style>
        body {{
            background: linear-gradient(to right, #4B0082, #8A2BE2);
            color: white;
        }}
        .title {{
            font-size: 50px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 20px;
            direction: rtl;
        }}
        .subtitle {{
            font-size: 30px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            direction: rtl;
        }}
        .rtl {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
        }}
        .stSelectbox, .stNumberInput {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stDataFrame {{
            direction: ltr;  /* الجداول تكون من اليسار إلى اليمين */
            text-align: left;
            font-size: 24px;
        }}
        /* تعديل الزائد والناقص في الأرقام */
        .stNumberInput > div > div > button {{
            margin-left: 0;
            margin-right: 5px;
        }}
        /* زر التمرير إلى الأعلى */
        .scroll-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            padding: 10px;
            font-size: 18px;
            cursor: pointer;
            display: none;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - حاسبة الدجاج</div>
        <div class="subtitle">حساب أرباح الدجاج والمكافآت اليومية</div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <style>
        body {{
            background: linear-gradient(to right, #4B0082, #8A2BE2);
            color: white;
        }}
        .title {{
            font-size: 50px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 20px;
            direction: ltr;
        }}
        .subtitle {{
            font-size: 30px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            direction: ltr;
        }}
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
        }}
        .stSelectbox, .stNumberInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stDataFrame {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
        }}
        /* زر التمرير إلى الأعلى */
        .scroll-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            padding: 10px;
            font-size: 18px;
            cursor: pointer;
            display: none;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Chicken Calculator</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
        """,
        unsafe_allow_html=True
    )

# زر التمرير إلى الأعلى
st.markdown(
    """
    <button onclick="scrollToTop()" class="scroll-top" id="scrollTopBtn" title="Go to top">↑</button>
    <script>
    // ظهور الزر عند التمرير لأسفل
    window.onscroll = function() {scrollFunction()};
    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("scrollTopBtn").style.display = "block";
        } else {
            document.getElementById("scrollTopBtn").style.display = "none";
        }
    }
    // التمرير إلى الأعلى
    function scrollToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
    </script>
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox("💰 العملة" if language == "العربية" else "💰 Currency", ["دولار" if language == "العربية" else "USD", "دينار عراقي" if language == "العربية" else "IQD"])

with col2:
    calculation_type = st.selectbox("📊 نوع الحساب" if language == "العربية" else "📊 Calculation Type", ["أرباح الدجاجة" if language == "العربية" else "Chicken Profits", "أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food"])

# قسم الحسابات
if calculation_type == "أرباح الدجاجة" or calculation_type == "Chicken Profits":
    st.subheader("📈 حساب أرباح الدجاجة" if language == "العربية" else "📈 Chicken Profits Calculation")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.number_input("🥚 عدد البيض" if language == "العربية" else "🥚 Number of Eggs", min_value=0, max_value=580, value=None, help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)", key="eggs")

    with col4:
        days = st.number_input("📅 عدد الأيام" if language == "العربية" else "📅 Number of Days", min_value=0, max_value=730, value=None, help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)", key="days")

    if st.button("🧮 احسب أرباح الدجاجة" if language == "العربية" else "🧮 Calculate Chicken Profits", type="primary"):
        if eggs is None or days is None:
            st.error("❗ يرجى إدخال جميع القيم المطلوبة!" if language == "العربية" else "❗ Please enter all required values!")
        elif eggs > 580:
            st.error("❗ عدد البيض يجب ألا يتجاوز 580!" if language == "العربية" else "❗ Number of eggs must not exceed 580!")
        elif days > 730:
            st.error("❗ عدد الأيام يجب ألا يتجاوز 730!" if language == "العربية" else "❗ Number of days must not exceed 730!")
        else:
            # حساب النتائج
            total_egg_price_usd = eggs * st.session_state.egg_price
            total_feed_cost_usd = (days * 2) * st.session_state.feed_price
            net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
            rent_cost_usd = 6.0
            net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

            if currency == "دينار عراقي" or currency == "IQD":
                total_egg_price = total_egg_price_usd * 1480
                total_feed_cost = total_feed_cost_usd * 1480
                net_profit_before_rent = net_profit_before_rent_usd * 1480
                rent_cost = rent_cost_usd * 1480
                net_profit = net_profit_usd * 1480
            else:
                total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                    total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
                )

            # عرض النتائج
            st.markdown(f"**إجمالي قيمة البيض**: {format_decimal(total_egg_price)} {currency}")
            st.markdown(f"**إجمالي تكلفة الطعام**: {format_decimal(total_feed_cost)} {currency}")
            st.markdown(f"**صافي الربح قبل الإيجار**: {format_decimal(net_profit_before_rent)} {currency}")
            st.markdown(f"**تكلفة الإيجار**: {format_decimal(rent_cost)} {currency}")
            st.markdown(f"**صافي الربح**: {format_decimal(net_profit)} {currency}")

# قسم المكافآت والطعام اليومي
elif calculation_type == "أرباح المكافآت والطعام اليومي" or calculation_type == "Daily Rewards and Food":
    st.subheader("🍗 حساب المكافآت والطعام اليومي" if language == "العربية" else "🍗 Daily Rewards and Food Calculation")
    col5, col6 = st.columns(2)

    with col5:
        daily_food = st.number_input("🍽️ كمية الطعام اليومي بالدينار" if language == "العربية" else "🍽️ Daily Food Quantity in IQD", min_value=0, max_value=100000, value=None, help="أدخل كمية الطعام اليومي" if language == "العربية" else "Enter the daily food quantity")

    with col6:
        reward_per_day = st.number_input("🎁 المكافأة اليومية" if language == "العربية" else "🎁 Daily Reward", min_value=0, max_value=10000, value=None, help="أدخل قيمة المكافأة اليومية" if language == "العربية" else "Enter the daily reward value")

    if st.button("🧮 احسب المكافآت والطعام اليومي" if language == "العربية" else "🧮 Calculate Daily Rewards and Food", type="primary"):
        if daily_food is None or reward_per_day is None:
            st.error("❗ يرجى إدخال جميع القيم المطلوبة!" if language == "العربية" else "❗ Please enter all required values!")
        else:
            # حساب المكافآت والطعام اليومي
            total_food_cost = daily_food * days
            total_rewards = reward_per_day * days

            st.markdown(f"**إجمالي تكلفة الطعام**: {format_decimal(total_food_cost)} {currency}")
            st.markdown(f"**إجمالي المكافآت اليومية**: {format_decimal(total_rewards)} {currency}")
