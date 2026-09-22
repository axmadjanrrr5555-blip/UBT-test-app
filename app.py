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
    </style>
""",
    unsafe_style_script=True,
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
    st.session_state.questions = []
if "time_limit" not in st.session_state:
    st.session_state.time_limit = 30
if "blocked_ips" not in st.session_state:
    st.session_state.blocked_ips = []
if "results" not in st.session_state:
    st.session_state.results = []
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

curr_time = time.time()

# Кіру блогы
if not st.session_state.logged_user:
    st.subheader("🔑 Кіру")
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

    # --- ТЕК ДИРЕКТОР ПАНЕЛІ ---
    if role == "director":
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📊 Логтар мен Нәтижелер",
                "🔑 Парольдер мен Ауыстыру",
                "🔓 Банды шешу",
                "🔐 ДИРЕКТОР / ЗАМ Пароль Ауыстыру",
            ]
        )
        with tab1:
            st.subheader("Тест тапсырғандар тізімі:")
            for r in st.session_state.results:
                st.write(
                    f"👤 {r['user']} | 🕒 {r['time']} | 📊 Уақыты: {r['duration']}сек | Балл: {r['score']}"
                )
        with tab2:
            st.subheader("Барлық логин мен парольдер:")
            st.json(st.session_state.users)
        with tab3:
            st.subheader("Банды алып тастау:")
            for u_name, u_data in st.session_state.users.items():
                if u_data["ban_until"] > curr_time:
                    if st.button(f"Unban: {u_name}"):
                        u_data["ban_until"] = 0
                        u_data["fails"] = 0
                        st.success(f"{u_name} баннан шығарылды!")
                        st.rerun()
        with tab4:
            st.subheader("🔑 Парольдерді өзгерту (Тек Директорға):")

            # Директордың өз паролін ауыстыруы
            st.write("---")
            st.write("**Өз пароліңізді ауыстыру (Директор):**")
            new_dir_pass = st.text_input(
                "Жаңа Директор паролі:", type="password", key="new_dir_p"
            )
            if st.button("Директор паролін жаңарту"):
                if new_dir_pass.strip():
                    st.session_state.users["director"]["pass"] = (
                        new_dir_pass.strip()
                    )
                    st.success("Директор паролі сәтті ауысты!")
                else:
                    st.warning("Пароль бос болмауы керек!")

            # Замның паролін ауыстыруы
            st.write("---")
            st.write("**Зам директордың паролін ауыстыру:**")
            new_zam_pass = st.text_input(
                "Жаңа Зам паролі:", type="password", key="new_zam_p"
            )
            if st.button("Зам паролін жаңарту"):
                if new_zam_pass.strip():
                    st.session_state.users["zam"]["pass"] = (
                        new_zam_pass.strip()
                    )
                    st.success("Зам директордың паролі сәтті ауысты!")
                else:
                    st.warning("Пароль бос болмауы керек!")

    # --- ЗАМДИРЕКТОР / ДИРЕКТОР БАСҚАРУЫ ---
    if role in ["director", "zam"]:
        st.subheader("⚙️ Басқару Панелі (Зам / Директор)")
        z_tab1, z_tab2, z_tab3 = st.tabs(
            ["📝 Сұрақ/Уақыт қосу", "👤 Оқушы қосу", "🚫 ПК Блоктау"]
        )
        with z_tab1:
            st.session_state.time_limit = st.number_input(
                "Тест уақыты (минут):",
                value=st.session_state.time_limit,
                min_value=1,
            )
            q_txt = st.text_input("Жаңа сұрақ:")
            q_ans = st.text_input("Дұрыс жауабы:")
            if st.button("Сұрақты сақтау"):
                st.session_state.questions.append(
                    {"q": q_txt, "a": q_ans}
                )
                st.success("Сұрақ қосылды!")
        with z_tab2:
            new_u = st.text_input("Оқушы логині:")
            new_p = st.text_input("Оқушы паролі:")
            if st.button("Оқушыны тіркеу"):
                st.session_state.users[new_u] = {
                    "pass": new_p,
                    "role": "student",
                    "fails": 0,
                    "ban_until": 0,
                }
                st.success("Оқушы қосылды!")
        with z_tab3:
            ip_to_block = st.text_input("Блоктайтын IP/ПК аты:")
            if st.button("ПК-ны блоктау"):
                st.session_state.blocked_ips.append(ip_to_block)
                st.success("ПК блокталды!")

    # --- ОҚУШЫ ТЕСТІ ---
    if role == "student":
        st.subheader("✍️ Тестілеу")
        score = 0
        start_t = time.time()
        for i, q in enumerate(st.session_state.questions):
            ans = st.text_input(f"{i+1}. {q['q']}", key=f"q_{i}")
            if ans.strip().lower() == q["a"].strip().lower():
                score += 1
        if st.button("Тестті аяқтау"):
            end_t = time.time()
            dur = int(end_t - start_t)
            st.session_state.results.append(
                {
                    "user": st.session_state.logged_user,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "duration": dur,
                    "score": score,
                }
            )
            st.success(f"Тест аяқталды! Нәтижеңіз: {score}")


