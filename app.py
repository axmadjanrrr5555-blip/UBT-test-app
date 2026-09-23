import streamlit as st

# Бет баптаулары
st.set_page_config(page_title="Kasum Ahmad", page_icon="🎓", layout="wide")

# CSS: Дәл суреттегідей фон (сызықтар, дөңгелектер) және "KASUM AHMAD" дизайны
st.markdown("""
<style>
    /* Негізгі фон және графикалық элементтер (круги & линиялар) */
    .stApp {
        background-color: #0c1527;
        background-image: 
            radial-gradient(circle at 8% 35%, transparent 60px, #1a365d 61px, #1a365d 65px, transparent 66px),
            radial-gradient(circle at 92% 55%, transparent 110px, #1a365d 111px, #1a365d 115px, transparent 116px),
            linear-gradient(135deg, transparent 45%, #1d4ed8 45.5%, #1d4ed8 46.5%, transparent 47%),
            linear-gradient(45deg, transparent 30%, #1d4ed8 30.5%, #1d4ed8 31.5%, transparent 32%),
            linear-gradient(125deg, transparent 70%, #1d4ed8 70.5%, #1d4ed8 71.5%, transparent 72%);
        background-attachment: fixed;
        color: #ffffff;
    }

    /* KASUM AHMAD тақырыбының дизайны */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 10%;
        width: 100%;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 3.2rem;
        font-weight: 900;
        color: #ffffff;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7), 0 0 30px rgba(255, 255, 255, 0.4);
        letter-spacing: 4px;
    }

    /* Инпут өрістерінің дизайны */
    .stTextInput > div > div > input {
        background-color: #162a45 !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 6px !important;
    }

    /* Батырманың дизайны */
    .stButton > button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        padding: 6px 20px;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }
</style>

<div class="header-container">
    <div class="header-title">KASUM</div>
    <div class="header-title">AHMAD</div>
</div>
""", unsafe_allow_html=True)

# Сессия жадын инициализациялау
if 'question_limit' not in st.session_state:
    st.session_state.question_limit = 10
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ----------------- АВТОРИЗАЦИЯ -----------------
if not st.session_state.logged_in:
    st.subheader("🔑 Кіру")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        username = st.text_input("Логин:")
        password = st.text_input("Пароль:", type="password")
        
        if st.button("Кіру"):
            if username == "director" and password == "123":
                st.session_state.logged_in = True
                st.session_state.user_role = "director"
                st.success("Директор болып кірдіңіз!")
                st.rerun()
            elif username == "zam" and password == "123":
                st.session_state.logged_in = True
                st.session_state.user_role = "zam"
                st.success("Зам болып кірдіңіз!")
                st.rerun()
            else:
                st.error("Логин немесе пароль қате!")

# ----------------- НЕГІЗГІ КАБИНЕТ -----------------
else:
    st.sidebar.write(f"**Ағымдағы пайдаланушы:** {st.session_state.user_role.upper()}")
    if st.sidebar.button("Жүйеден шығу"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()

    # ДИРЕКТОР КАБИНЕТІ
    if st.session_state.user_role == "director":
        st.header("👨‍💼 Директор кабинеті")
        
        st.subheader("⚙️ Сұрақтар лимитін басқару")
        c1, c2 = st.columns([2, 1])
        with c1:
            new_limit = st.number_input("Жаңа сұрақтар лимитін енгізіңіз:", min_value=1, value=st.session_state.question_limit)
        with c2:
            st.write("")
            st.write("")
            if st.button("Лимитті сақтау"):
                st.session_state.question_limit = int(new_limit)
                st.success(f"Лимит {new_limit} сұраққа өзгертілді!")

        st.info(f"📊 Жалпы лимит: **{st.session_state.question_limit}** | Еңгізілген сұрақтар: **{len(st.session_state.questions)}**")
        st.divider()

        st.subheader("➕ Бір дұрыс жауабы бар сұрақ қосу")
        
        if len(st.session_state.questions) >= st.session_state.question_limit:
            st.warning("⚠️ Сұрақтар лимиті толды!")
        else:
            q_text = st.text_area("Сұрақ мәтіні:", key="single_q")
            opt_a = st.text_input("A варианты:", key="s_a")
            opt_b = st.text_input("B варианты:", key="s_b")
            opt_c = st.text_input("C варианты:", key="s_c")
            opt_d = st.text_input("D варианты:", key="s_d")
            
            correct_opt = st.radio("Дұрыс вариантты таңдаңыз:", ["A", "B", "C", "D"])

            if st.button("Сұрақты сақтау (Директор)"):
                if q_text and opt_a and opt_b and opt_c and opt_d:
                    opts = [opt_a, opt_b, opt_c, opt_d]
                    correct_idx = ["A", "B", "C", "D"].index(correct_opt)
                    
                    st.session_state.questions.append({
                        "type": "Бір жауапты",
                        "author": "Директор",
                        "question": q_text,
                        "options": opts,
                        "correct": [correct_idx]
                    })
                    st.success("Сұрақ сәтті қосылды!")
                    st.rerun()
                else:
                    st.error("Барлық өрістерді толтырыңыз!")

    # ЗАМ (ОРЫНБАСАР) КАБИНЕТІ
    elif st.session_state.user_role == "zam":
        st.header("🧑‍💼 Зам кабинеті")
        st.info(f"📊 Директор белгілеген лимит: **{st.session_state.question_limit}** | Еңгізілген сұрақтар: **{len(st.session_state.questions)}**")
        st.divider()

        st.subheader("➕ Бірнеше дұрыс жауабы бар сұрақ қосу")

        if len(st.session_state.questions) >= st.session_state.question_limit:
            st.warning("⚠️ Директор белгілеген сұрақтар лимиті толды!")
        else:
            q_text = st.text_area("Сұрақ мәтіні:", key="multi_q")
            
            col_a, col_b = st.columns([3, 1])
            with col_a: opt_a = st.text_input("A варианты:", key="m_a")
            with col_b: chk_a = st.checkbox("Дұрыс A", key="cb_a")

            with col_a: opt_b = st.text_input("B варианты:", key="m_b")
            with col_b: chk_b = st.checkbox("Дұрыс B", key="cb_b")

            with col_a: opt_c = st.text_input("C варианты:", key="m_c")
            with col_b: chk_c = st.checkbox("Дұрыс C", key="cb_c")

            with col_a: opt_d = st.text_input("D варианты:", key="m_d")
            with col_b: chk_d = st.checkbox("Дұрыс D", key="cb_d")

            if st.button("Сұрақты сақтау (Зам)"):
                corrects = []
                if chk_a: corrects.append(0)
                if chk_b: corrects.append(1)
                if chk_c: corrects.append(2)
                if chk_d: corrects.append(3)

                if q_text and opt_a and opt_b and opt_c and opt_d:
                    if len(corrects) == 0:
                        st.error("Кем дегенде бір дұрыс жауапты белгілеңіз!")
                    else:
                        opts = [opt_a, opt_b, opt_c, opt_d]
                        st.session_state.questions.append({
                            "type": "Бірнеше жауапты",
                            "author": "Зам",
                            "question": q_text,
                            "options": opts,
                            "correct": corrects
                        })
                        st.success("Сұрақ сәтті қосылды!")
                        st.rerun()
                else:
                    st.error("Барлық өрістерді толтырыңыз!")

    # СҰРАҚТАР ТІЗІМІ
    st.divider()
    st.subheader("📋 Қосылған сұрақтар тізімі")
    if len(st.session_state.questions) == 0:
        st.write("Әлі ешқандай сұрақ қосылмаған.")
    else:
        for idx, q in enumerate(st.session_state.questions):
            with st.expander(f"{idx+1}. {q['question']} ({q['author']} - {q['type']})"):
                for o_idx, opt in enumerate(q['options']):
                    if o_idx in q['correct']:
                        st.markdown(f"- **{opt}** ✅ *(Дұрыс жауап)*")
                    else:
                        st.markdown(f"- {opt}")
