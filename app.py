import time
from datetime import datetime
import streamlit as st

# Экран қара, жазулар жасыл стиль
st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: #00FF00; }
    h1, h2, h3, h4, h5, h6, p, label, div, span, input { color: #00FF00 !important; }
    .stButton>button { background-color: #111; color: #00FF00; border: 1px solid #00FF00; }
    .stRadio label { color: #00FF00 !important; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🟢 ҰБТ Басқару Жүйесі")

# Базаны баптау
if "users" not in st.session_state:
    st.session_state.users = {
        "director": {
            "pass": "dir123",
            "role": "director",
            "fails": 0,
            "ban_until": 0,
        },
        "zam": {"pass": "zam123", "role": "zam", "fails": 0, "ban_until": 0},
    }

if "questions" not in st.session_state:
    # Пәндер бойынша сұрақтар базасы
    st.session_state.questions = {
        "Математика": [],
        "Қазақстан тарихы": [],
        "Оқу сауаттылығы": [],
    }

if "login_logs" not in st.session_state:
    st.session_state.login_logs = []  # Қай ПК/Логин қашан кірді

if "can_zam_add_q" not in st.session_state:
    st.session_state.can_zam_add_q = True  # Замға сұрақ қосу рұқсаты

if "results" not in st.session_state:
    st.session_state.results = []

if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

curr_time = time.time()

# Кіру блогы
if not st.session_state.logged_user:
    st.subheader("🔑 Жүйеге кіру")
    login = st.text_input("Логин:")
    password = st.text_input("Пароль:", type="password")

    if st.button("Кіру"):
        if login in st.session_state.users:
            usr = st.session_state.users[login]
            if usr["ban_until"] > curr_time:
                left = int((usr["ban_until"] - curr_time) // 60)
                st.error(f"⛔ Блокталғансыз! {left} мин қалды.")
            elif usr["pass"] == password:
                usr["fails"] = 0
                st.session_state.logged_user = login

                # Кіру кім, қашан жасағанын логқа жазу (Тек Директор көреді)
                login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.login_logs.append(
                    {"user": login, "time": login_time, "role": usr["role"]}
                )

                st.rerun()
            else:
                usr["fails"] += 1
                if usr["fails"] >= 5:
                    usr["ban_until"] = curr_time + 1800
                    st.error("⛔ Пароль 5 рет қате жазылды! 30 мин бан.")
                else:
                    st.error(f"❌ Қате пароль! Қалған мүмкіндік: {5 - usr['fails']}")
        else:
            st.error("❌ Мұндай қолданушы жоқ!")

else:
    user_info = st.session_state.users[st.session_state.logged_user]
    role = user_info["role"]
    st.sidebar.write(
        f"Пайдаланушы: **{st.session_state.logged_user}** ({role.upper()})"
    )
    if st.sidebar.button("Шығу"):
        st.session_state.logged_user = None
        st.rerun()

    # ==================== ТЕК ДИРЕКТОР ПАНЕЛІ ====================
    if role == "director":
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "🖥️ ПК/Кіру Тарихы (Логтар)",
                "🔑 Барлық Логин/Парольдер",
                "📊 Тест Нәтижелері",
                "🔓 Банды Шешу",
                "🔐 Пароль Ауыстыру & Доступ",
            ]
        )

        with tab1:
            st.subheader("🖥️ Жүйеге кірген ПК мен пайдаланушылар уақыты:")
            for log in reversed(st.session_state.login_logs):
                st.write(
                    f"⏰ **{log['time']}** | 👤 Логин: `{log['user']}` ({log['role']})"
                )

        with tab2:
            st.subheader("🔑 Зам және Оқушылардың парольдері:")
            st.json(st.session_state.users)

        with tab3:
            st.subheader("📊 Оқушылардың тест нәтижелері:")
            for r in st.session_state.results:
                st.write(
                    f"👤 {r['user']} | 📚 Пән: {r['subject']} | 🕒 {r['time']} | Балл: {r['score']}"
                )

        with tab4:
            st.subheader("🔓 Банды алып тастау:")
            for u_name, u_data in st.session_state.users.items():
                if u_data["ban_until"] > curr_time:
                    if st.button(f"Unban: {u_name}"):
                        u_data["ban_until"] = 0
                        u_data["fails"] = 0
                        st.success(f"{u_name} баннан шығарылды!")
                        st.rerun()

        with tab5:
            st.subheader("⚙️ Доступ және Парольдерді басқару:")

            # Замға сұрақ қосу доступ беру/алу
            allow_zam = st.checkbox(
                "Зам директорға сұрақ қосуға доступ беру",
                value=st.session_state.can_zam_add_q,
            )
            st.session_state.can_zam_add_q = allow_zam

            st.write("---")
            # Директордың өз паролін ауыстыруы
            new_dir_p = st.text_input(
                "Жаңа Директор паролі:", type="password", key="np_dir"
            )
            if st.button("Директор паролін жаңарту"):
                if new_dir_p.strip():
                    st.session_state.users["director"]["pass"] = (
                        new_dir_p.strip()
                    )
                    st.success("Ауыстырылды!")

            # Замның паролін ауыстыруы
            new_zam_p = st.text_input(
                "Жаңа Зам паролі:", type="password", key="np_zam"
            )
            if st.button("Зам паролін жаңарту"):
                if new_zam_p.strip():
                    st.session_state.users["zam"]["pass"] = new_zam_p.strip()
                    st.success("Ауыстырылды!")

    # ==================== СҰРАҚ ҚОСУ БАСҚАРУЫ (ДИРЕКТОР / ЗАМ) ====================
    if role == "director" or (role == "zam"):
        st.subheader("⚙️ Басқару Панелі")
        z_tab1, z_tab2 = st.tabs(["📝 Сұрақ Құрастыру (4 вариант)", "👤 Оқушы Қосу"])

        with z_tab1:
            if role == "zam" and not st.session_state.can_zam_add_q:
                st.error(
                    "⛔ Директор сізге сұрақ қосу рұқсатын жауып тастаған!"
                )
            else:
                st.write("**Жаңа сұрақ енгізу (A, B, C, D нұсқаларымен):**")
                selected_sub = st.selectbox(
                    "Пәнді таңдаңыз:", list(st.session_state.questions.keys())
                )
                q_text = st.text_input("Сұрақты жазыңыз:")

                col1, col2 = st.columns(2)
                with col1:
                    opt_a = st.text_input("A жауабы:")
                    opt_b = st.text_input("B жауабы:")
                with col2:
                    opt_c = st.text_input("C жауабы:")
                    opt_d = st.text_input("D жауабы:")

                correct_opt = st.radio(
                    "Қай нұсқа ДҰРЫС?", ["A", "B", "C", "D"], horizontal=True
                )

                if st.button("Сұрақты сақтау"):
                    if q_text and opt_a and opt_b and opt_c and opt_d:
                        st.session_state.questions[selected_sub].append(
                            {
                                "q": q_text,
                                "options": {
                                    "A": opt_a,
                                    "B": opt_b,
                                    "C": opt_c,
                                    "D": opt_d,
                                },
                                "correct": correct_opt,
                            }
                        )
                        st.success("Сұрақ сәтті қосылды!")
                    else:
                        st.warning("Барлық өрістерді толтырыңыз!")

        with z_tab2:
            st.write("**Жаңа оқушы тіркеу:**")
            new_st_u = st.text_input("Оқушы логині:")
            new_st_p = st.text_input("Оқушы паролі:")
            if st.button("Оқушыны сақтау"):
                if new_st_u and new_st_p:
                    st.session_state.users[new_st_u] = {
                        "pass": new_st_p,
                        "role": "student",
                        "fails": 0,
                        "ban_until": 0,
                    }
                    st.success(f"Оқушы {new_st_u} қосылды!")

    # ==================== ОҚУШЫ ТЕСТІ ====================
    if role == "student":
        st.subheader("✍️ Тестілеу Бөлімі")

        # Пән таңдау
        subject = st.selectbox(
            "Қай пәннен тест тапсырасыз?",
            list(st.session_state.questions.keys()),
        )

        q_list = st.session_state.questions[subject]

        if not q_list:
            st.info("Бұл пән бойынша әлі сұрақтар қосылмаған.")
        else:
            st.write(f"--- \n ### 📚 Пән: {subject}")
            user_answers = {}

            for i, q in enumerate(q_list):
                st.write(f"**{i+1}. {q['q']}**")
                opts = q["options"]
                formatted_opts = [f"{k}) {v}" for k, v in opts.items()]
                ans = st.radio(
                    "Жауапты таңдаңыз:", formatted_opts, key=f"q_{subject}_{i}"
                )
                user_answers[i] = ans[0]  # Алынған 'A', 'B', 'C' немесе 'D'

            if st.button("Тестті аяқтау және тапсыру"):
                score = 0
                for i, q in enumerate(q_list):
                    if user_answers.get(i) == q["correct"]:
                        score += 1

                test_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.results.append(
                    {
                        "user": st.session_state.logged_user,
                        "subject": subject,
                        "time": test_time,
                        "score": f"{score}/{len(q_list)}",
                    }
                )
                st.success(
                    f"Тест аяқталды! Сіздің нәтижеңіз: {score} / {len(q_list)}"
                )
