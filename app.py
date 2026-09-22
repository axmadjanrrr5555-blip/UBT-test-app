from datetime import datetime
import time
import pandas as pd
import streamlit as st

st.set_page_config(page_title="KASUM AHMAD", layout="wide")

# Көк-сұр фон және БАРЛЫҚ МӘТІНДЕРДІ АШЫҚ ЖАСЫЛ (НЕОН) КЫЛУ CSS-і
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main-title {
        font-size: 80px;
        font-weight: 800;
        letter-spacing: 5px;
        color: #39ff14 !important;
        margin-bottom: 0px;
        line-height: 1;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }
    
    .sub-title {
        font-size: 80px;
        font-weight: 800;
        letter-spacing: 5px;
        color: #39ff14 !important;
        text-align: right;
        margin-top: 0px;
        line-height: 1;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
    }
    
    /* Барлық сөздерді, тақырыптарды және жазуларды ашық жасыл қылу */
    h1, h2, h3, h4, h5, h6, p, label, div, span, input, button, small, li { 
        color: #39ff14 !important; 
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    /* Батырмалардың жасыл стилі */
    .stButton>button { 
        background-color: rgba(0, 0, 0, 0.6) !important; 
        color: #39ff14 !important; 
        border: 2px solid #39ff14 !important; 
        border-radius: 8px;
        font-size: 16px !important;
    }

    /* Input және Selectbox жасыл түсі */
    .stTextInput>div>div>input {
        color: #39ff14 !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid #39ff14 !important;
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
        "Математика": [
            {
                "q": "2 + 2 = ?",
                "options": {
                    "A": "3",
                    "B": "4",
                    "C": "5",
                    "D": "6",
                    "E": "",
                    "F": "",
                },
                "correct": ["B"],
                "image": "",
            }
        ],
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
                img_url = st.text_input(
                    "🖼️ Сұраққа сурет сілтемесі (міндетті емес URL):"
                )

                st.write("Варианттар (А-дан F-ке дейін):")
                col1, col2 = st.columns(2)
                with col1:
                    opt_a = st.text_input("A жауабы:")
                    opt_b = st.text_input("B жауабы:")
                    opt_c = st.text_input("C жауабы:")
                with col2:
                    opt_d = st.text_input("D жауабы:")
                    opt_e = st.text_input("E жауабы (міндетті емес):")
                    opt_f = st.text_input("F жауабы (міндетті емес):")

                st.write("Дұрыс жауап(тар)ды белгілеңіз (3-ке дейін):")
                corr_a = st.checkbox("A дұрыс")
                corr_b = st.checkbox("B дұрыс")
                corr_c = st.checkbox("C дұрыс")
                corr_d = st.checkbox("D дұрыс")
                corr_e = st.checkbox("E дұрыс")
                corr_f = st.checkbox("F дұрыс")

                correct_selected = []
                if corr_a:
                    correct_selected.append("A")
                if corr_b:
                    correct_selected.append("B")
                if corr_c:
                    correct_selected.append("C")
                if corr_d:
                    correct_selected.append("D")
                if corr_e:
                    correct_selected.append("E")
                if corr_f:
                    correct_selected.append("F")

                if st.button("Сұрақты сақтау"):
                    # Егер 4-тен көп вариант толтырылмаса (E мен F бос болса) -> Автоматты 1 дұрыс жауап
                    has_extra_opts = bool(
                        opt_e.strip() != "" or opt_f.strip() != ""
                    )

                    if not q_text or not (opt_a and opt_b and opt_c and opt_d):
                        st.error("⚠️ А, B, C, D варианттары мен сұрақ міндетті түрде толтырылуы керек!")
                    elif len(correct_selected) == 0:
                        st.error("⚠️ Кемінде 1 дұрыс жауапты белгілеңіз!")
                    elif len(correct_selected) > 3:
                        st.error("⚠️ Дұрыс жауаптар саны 3-тен аспауы керек!")
                    elif not has_extra_opts and len(correct_selected) > 1:
                        st.error("⚠️ 4 вариантты тестіде тек 1 дұрыс жауап болуы тиіс!")
                    else:
                        st.session_state.questions[selected_sub].append(
                            {
                                "q": q_text,
                                "options": {
                                    "A": opt_a,
                                    "B": opt_b,
                                    "C": opt_c,
                                    "D": opt_d,
                                    "E": opt_e,
                                    "F": opt_f,
                                },
                                "correct": correct_selected,
                                "image": img_url.strip(),
                            }
                        )
                        st.success("✅ Сұрақ сәтті қосылды!")

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

    # --- ОҚУШЫ ТЕСТІ (СУРЕТТЕР ВАРИАНТТАР БАР) ---
    if role == "student":
        subject = st.selectbox(
            "Пән таңдаңыз:", list(st.session_state.questions.keys())
        )
        q_list = st.session_state.questions[subject]

        if q_list:
            user_answers = {}
            for i, q in enumerate(q_list):
                st.write(f"**{i+1}. {q['q']}**")

                # Сурет бар болса көрсету
                if q.get("image"):
                    st.image(q["image"], use_column_width=True)

                opts = q["options"]
                # Бос емес варианттарды таңдау
                available_opts = {k: v for k, v in opts.items() if v.strip()}

                # Егер 4 вариантты тест болса (1 дұрыс жауап) -> Radio button
                if len(available_opts) <= 4 or len(q["correct"]) == 1:
                    formatted_opts = [
                        f"{k}) {v}" for k, v in available_opts.items()
                    ]
                    ans = st.radio(
                        "Жауапты таңдаңыз:",
                        formatted_opts,
                        key=f"q_{subject}_{i}",
                    )
                    user_answers[i] = [ans[0]]
                else:
                    # Көп жауапты тест -> Checkboxes
                    st.write("Көп жауапты тест (бірнешеуін таңдауға болады):")
                    selected_list = []
                    for k, v in available_opts.items():
                        cb = st.checkbox(
                            f"{k}) {v}", key=f"q_{subject}_{i}_{k}"
                        )
                        if cb:
                            selected_list.append(k)
                    user_answers[i] = selected_list

            if st.button("Тестті аяқтау"):
                score = 0
                for i, q in enumerate(q_list):
                    u_ans = set(user_answers.get(i, []))
                    c_ans = set(q["correct"])
                    if u_ans == c_ans and len(u_ans) > 0:
                        score += 1

                wrong_score = len(q_list) - score

                st.session_state.results.append(
                    {
                        "user": st.session_state.logged_user,
                        "subject": subject,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "score": f"{score}/{len(q_list)}",
                    }
                )

                st.success(f"Нәтиже: {score} / {len(q_list)}")

                # --- ГРАФИК КӨРСЕТУ ---
                st.subheader("📊 Тест Нәтижесінің Графигі")
                chart_data = pd.DataFrame(
                    {
                        "Көрсеткіш": ["Дұрыс", "Қате"],
                        "Саны": [score, wrong_score],
                    }
                )
                st.bar_chart(chart_data.set_index("Көрсеткіш"))
