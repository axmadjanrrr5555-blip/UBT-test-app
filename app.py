import time
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="KASUM AHMAD", layout="wide")

# Жіберілген көк-сұр текстуралық фонды қосу
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.magnific.com/fotos-premium/vista-panoramica-lago-montanas-contra-cielo_1048944-656242.jpg?semt=ais_hybrid&w=740");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main-title {
        font-size: 80px;
        font-weight: 800;
        letter-spacing: 5px;
        color: #ffffff;
        margin-bottom: 0px;
        line-height: 1;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.6);
    }
    
    .sub-title {
        font-size: 80px;
        font-weight: 800;
        letter-spacing: 5px;
        color: #ffffff;
        text-align: right;
        margin-top: 0px;
        line-height: 1;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.6);
    }
    
    h1, h2, h3, h4, h5, h6, p, label, div, span, input { 
        color: #ffffff !important; 
        text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
    }
    
    .stButton>button { 
        background-color: rgba(0, 0, 0, 0.4); 
        color: #ffffff; 
        border: 1px solid #ffffff; 
        border-radius: 5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">KASUM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AHMAD</div>', unsafe_allow_html=True)
st.write("---")

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
    st.session_state.questions = {
        "Математика": [],
        "Қазақстан тарихы": [],
        "Оқу сауаттылығы": [],
    }

if "login_logs" not in st.session_state:
    st.session_state.login_logs = []

if "can_zam_add_q" not in st.session_state:
    st.session_state.can_zam_add_q = True

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

    # --- ДИРЕКТОР ПАНЕЛІ ---
    if role == "director":
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "🖥️ ПК/Кіру Тарихы",
                "🔑 Логин/Парольдер",
                "📊 Тест Нәтижелері",
                "🔓 Банды Шешу",
                "🔐 Пароль & Доступ",
            ]
        )

        with tab1:
            for log in reversed(st.session_state.login_logs):
                st.write(
                    f"⏰ **{log['time']}** | 👤 Логин: `{log['user']}` ({log['role']})"
                )

        with tab2:
            st.json(st.session_state.users)

        with tab3:
            for r in st.session_state.results:
                st.write(
                    f"👤 {r['user']} | 📚 Пән: {r['subject']} | 🕒 {r['time']} | Балл: {r['score']}"
                )

        with tab4:
            for u_name, u_data in st.session_state.users.items():
                if u_data["ban_until"] > curr_time:
                    if st.button(f"Unban: {u_name}"):
                        u_data["ban_until"] = 0
                        u_data["fails"] = 0
                        st.success(f"{u_name} баннан шығарылды!")
                        st.rerun()

        with tab5:
            allow_zam = st.checkbox(
                "Зам директорға сұрақ қосуға доступ беру",
                value=st.session_state.can_zam_add_q,
            )
            st.session_state.can_zam_add_q = allow_zam

            new_dir_p = st.text_input(
                "Жаңа Директор паролі:", type="password", key="np_dir"
            )
            if st.button("Директор паролін жаңарту"):
                if new_dir_p.strip():
                    st.session_state.users["director"]["pass"] = (
                        new_dir_p.strip()
                    )
                    st.success("Ауыстырылды!")

            new_zam_p = st.text_input(
                "Жаңа Зам паролі:", type="password", key="np_zam"
            )
            if st.button("Зам паролін жаңарту"):
                if new_zam_p.strip():
                    st.session_state.users["zam"]["pass"] = new_zam_p.strip()
                    st.success("Ауыстырылды!")

    # --- ЗАМ/ДИРЕКТОР СҰРАҚ ҚОСУ ---
    if role == "director" or role == "zam":
        st.subheader("⚙️ Басқару Панелі")
        z_tab1, z_tab2 = st.tabs(["📝 Сұрақ Құрастыру", "👤 Оқушы Қосу"])

        with z_tab1:
            if role == "zam" and not st.session_state.can_zam_add_q:
                st.error("⛔ Доступ жабық!")
            else:
                selected_sub = st.selectbox(
                    "Пән:", list(st.session_state.questions.keys())
                )
                q_text = st.text_input("Сұрақ:")
                col1, col2 = st.columns(2)
                with col1:
                    opt_a = st.text_input("A жауабы:")
                    opt_b = st.text_input("B жауабы:")
                with col2:
                    opt_c = st.text_input("C жауабы:")
                    opt_d = st.text_input("D жауабы:")
                correct_opt = st.radio(
                    "Дұрыс нұсқа:", ["A", "B", "C", "D"], horizontal=True
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
                        st.success("Сұрақ қосылды!")

        with z_tab2:
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
                    st.success("Оқушы қосылды!")

    # --- ОҚУШЫ ТЕСТІ ---
    if role == "student":
        subject = st.selectbox(
            "Пән таңдаңыз:", list(st.session_state.questions.keys())
        )
        q_list = st.session_state.questions[subject]

        if q_list:
            user_answers = {}
            for i, q in enumerate(q_list):
                st.write(f"**{i+1}. {q['q']}**")
                opts = q["options"]
                formatted_opts = [f"{k}) {v}" for k, v in opts.items()]
                ans = st.radio(
                    "Жауап:", formatted_opts, key=f"q_{subject}_{i}"
                )
                user_answers[i] = ans[0]

            if st.button("Тестті аяқтау"):
                score = sum(
                    1
                    for i, q in enumerate(q_list)
                    if user_answers.get(i) == q["correct"]
                )
                st.session_state.results.append(
                    {
                        "user": st.session_state.logged_user,
                        "subject": subject,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "score": f"{score}/{len(q_list)}",
                    }
                )
                st.success(f"Нәтиже: {score} / {len(q_list)}")
