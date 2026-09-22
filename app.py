import streamlit as st

# Настройки страницы
st.set_page_config(page_title="Қасым Ахмад", page_icon="🎓", layout="wide")

# CSS стили с заголовками по углам
st.markdown("""
<style>
    .stApp {
        background-color: #121824;
        color: #ffffff;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        width: 100%;
        margin-bottom: 30px;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        color: #adff2f;
        text-shadow: 0 0 10px rgba(173, 255, 47, 0.4);
        letter-spacing: 2px;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
</style>

<div class="header-container">
    <div class="header-title">ҚАСЫМ</div>
    <div class="header-title">АХМАД</div>
</div>
""", unsafe_allow_html=True)

# Инициализация состояния
if 'question_limit' not in st.session_state:
    st.session_state.question_limit = 10
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# ----------------- ФОРМА ВХОДА -----------------
if not st.session_state.logged_in:
    st.subheader("🔑 Жүйеге кіру")
    
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

# ----------------- ЛИЧНЫЙ КАБИНЕТ -----------------
else:
    st.sidebar.write(f"**Ағымдағы пайдаланушы:** {st.session_state.user_role.upper()}")
    if st.sidebar.button("Жүйеден шығу"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()

    # КАБИНЕТ ДИРЕКТОРА
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

    # КАБИНЕТ ЗАМА
    elif st.session_state.user_role == "zam":
        st.header("🧑‍💼 Зам (Орынбасар) кабинеті")
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

    # СПИСОК ВОПРОСОВ
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
