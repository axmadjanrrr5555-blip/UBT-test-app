from datetime import datetime
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ONLINE TEST SYSTEM", layout="wide", page_icon="📜"
)

# TRADINGVIEW / BINANCE DARK STYLE CSS (ЭКРАНДЫ 80% ЖӘНЕ СҰРАҚТАРДЫ 60% ЕТУ)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14 !important;
        background-image: radial-gradient(circle at 50% 20%, #131722 0%, #0b0e14 100%);
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
    }
    
    /* БАҒДАРЛАМА ЕКРАННЫҢ 80%-ЫН АЛАДЫ */
    .block-container {
        max-width: 80% !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }
    
    .main-title {
        font-size: 60px;
        font-weight: 900;
        letter-spacing: 4px;
        color: #00FF66 !important;
        margin-bottom: 0px;
        line-height: 1;
        text-shadow: 0 0 20px rgba(0, 255, 102, 0.5);
    }
    
    .sub-title {
        font-size: 60px;
        font-weight: 900;
        letter-spacing: 4px;
        color: #00FF66 !important;
        text-align: right;
        margin-top: 0px;
        line-height: 1;
        text-shadow: 0 0 20px rgba(0, 255, 102, 0.5);
    }

    .welcome-text {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #00FF66 !important;
        background: #131722;
        padding: 12px 20px;
        border-radius: 8px;
        border-left: 5px solid #00FF66;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.2);
    }

    /* СҰРАҚТАР БӨЛІМІ ЕКРАННЫҢ 60%-ЫН АЛАДЫ ЖӘНЕ ҮЛКЕН ШРИФТПЕН БОЛАДЫ */
    .question-box {
        width: 60% !important;
        margin: 0 auto 30px auto;
        background: #131722;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #2a2e39;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.1);
    }
    
    .question-box h4, .question-box p, .question-box label {
        font-size: 22px !important;
        color: #D1D4DC !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span, small, li { 
        color: #D1D4DC !important; 
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00FF66 !important;
        font-size: 32px !important;
        font-weight: bold;
    }

    .stButton>button { 
        background: linear-gradient(135deg, #1e222d 0%, #2a2e39 100%) !important; 
        color: #00FF66 !important; 
        border: 1.5px solid #00FF66 !important; 
        border-radius: 6px;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
    }
    
    .stButton>button:hover {
        background: #00FF66 !important;
        color: #0b0e14 !important;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.8);
    }

    .stTextInput>div>div>input, .stSelectbox>div>div {
        color: #00FF66 !important;
        background-color: #1e222d !important;
        border: 1px solid #2a2e39 !important;
        border-radius: 6px;
        font-size: 18px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #131722;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #848e9c !important;
        font-size: 18px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00FF66 !important;
        border-bottom: 2px solid #00FF66 !important;
    }

    /* СЕРТИФИКАТ СТИЛІ */
    .certificate-box {
        border: 10px solid #00FF66;
        padding: 40px;
        background: #131722;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 102, 0.3);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .cert-title {
        font-size: 45px !important;
        font-weight: 900 !important;
        color: #00FF66 !important;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .cert-academy {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #848e9c !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 25px;
    }
    .cert-name {
        font-size: 42px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        border-bottom: 3px solid #00FF66;
        display: inline-block;
        padding-bottom: 8px;
        margin: 20px 0;
        letter-spacing: 2px;
    }
    .cert-body {
        font-size: 22px !important;
        color: #D1D4DC !important;
        margin: 12px 0;
    }
    .cert-score {
        font-size: 45px !important;
        font-weight: bold !important;
        color: #00FF66 !important;
        margin: 10px 0;
    }
    .cert-rank {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #FFD700 !important;
        background: #1e222d;
        display: inline-block;
        padding: 10px 25px;
        border-radius: 8px;
        border: 1.5px solid #FFD700;
        margin: 18px 0;
    }
    .cert-footer {
        display: flex;
        justify-content: space-between;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px dashed #2a2e39;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">ONLINE TEST</div>', unsafe_allow_html=True
)
st.markdown('<div class="sub-title">PORTAL</div>', unsafe_allow_html=True)
st.write("---")

# Session State баптаулары (Барлық мектеп пәндері қосылды)
if "users" not in st.session_state:
    st.session_state.users = {
        "director": {
            "name": "Қасым Ахмад (Директор)",
            "pass": "dir123",
            "role": "director",
            "fails": 0,
            "ban_until": 0,
            "attempts": 9999,
        },
        "zam": {
            "name": "Зам Директор",
            "pass": "zam123",
            "role": "zam",
            "fails": 0,
            "ban_until": 0,
            "attempts": 9999,
        },
    }

if "questions" not in st.session_state:
    st.session_state.questions = {
        "Математика": [],
        "Қазақстан тарихы": [],
        "Оқу сауаттылығы": [],
        "Физика": [],
        "Химия": [],
        "Биология": [],
        "География": [],
        "Информатика": [],
        "Қазақ тілі": [],
        "Қазақ әдебиеті": [],
        "Ағылшын тілі": [],
        "Дүниежүзі тарихы": [],
        "Адам. Қоғам. Құқық": [],
    }

if "login_logs" not in st.session_state:
    st.session_state.login_logs = []

if "results" not in st.session_state:
    st.session_state.results = []

if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

if "last_cert" not in st.session_state:
    st.session_state.last_cert = None

if "review_result" not in st.session_state:
    st.session_state.review_result = None

if "selected_exam_subject" not in st.session_state:
    st.session_state.selected_exam_subject = None

curr_time = time.time()

# --- КІРУ БӨЛІМІ ---
if not st.session_state.logged_user:
    st.subheader("🔑 Жүйеге Кіру")
    col1, col2 = st.columns([1, 1])
    with col1:
        login = st.text_input("Логин:")
        password = st.text_input("Пароль:", type="password")

        if st.button("Кіру / Login"):
            if login in st.session_state.users:
                usr = st.session_state.users[login]
                if usr["ban_until"] > curr_time:
                    left = int((usr["ban_until"] - curr_time) // 60)
                    st.error(
                        f"⛔ Блокталғансыз! Пароль 10 рет қате терілді. {left} мин қалды."
                    )
                elif usr["pass"] == password:
                    if usr["role"] == "student" and usr.get("attempts", 0) <= 0:
                        st.error(
                            "⛔ Сізде тест тапсыруға доступ жоқ! Директордан немесе Замнан минут сұраңыз."
                        )
                    else:
                        usr["fails"] = 0
                        st.session_state.logged_user = login
                        st.session_state.last_cert = None
                        st.session_state.review_result = None
                        st.session_state.selected_exam_subject = None
                        login_time = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        st.session_state.login_logs.append(
                            {
                                "user": usr.get("name", login),
                                "username": login,
                                "time": login_time,
                                "role": usr["role"],
                            }
                        )
                        st.rerun()
                else:
                    usr["fails"] += 1
                    if usr["fails"] >= 10:
                        usr["ban_until"] = curr_time + 1800
                        st.error(
                            "⛔ 10 рет қате пароль енгізілді! Аккаунт 30 минутқа БАНДАЛДЫ."
                        )
                    else:
                        st.error(
                            f"❌ Қате пароль! Қалған мүмкіндік: {10 - usr['fails']}"
                        )
            else:
                st.error("❌ Мұндай қолданушы тіркелмеген!")

else:
    user_info = st.session_state.users[st.session_state.logged_user]
    role = user_info["role"]
    full_name = user_info.get("name", st.session_state.logged_user)

    st.markdown(
        f'<div class="welcome-text">👋 Welcome, {full_name}!</div>',
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(f"📈 **Аты-жөні:** `{full_name}`")
    st.sidebar.markdown(f"👤 **Логин:** `{st.session_state.logged_user}`")
    st.sidebar.markdown(
        f"🏷️ **Статус:** `<span style='color:#00FF66'>{role.upper()}</span>`",
        unsafe_allow_html=True,
    )

    if role == "student":
        st.sidebar.markdown(
            f"🔑 **Қалған доступ:** `{user_info.get('attempts', 0)}`"
        )
        if st.session_state.selected_exam_subject:
            st.sidebar.markdown(
                f"📚 **Таңдалған пән:** `{st.session_state.selected_exam_subject}`"
            )
            if st.sidebar.button("🔄 Басқа пән таңдау"):
                st.session_state.selected_exam_subject = None
                st.rerun()

    if st.sidebar.button("Шығу / Logout"):
        st.session_state.logged_user = None
        st.session_state.last_cert = None
        st.session_state.review_result = None
        st.session_state.selected_exam_subject = None
        st.rerun()

    # --- ДИРЕКТОР ПАНЕЛІ ---
    if role == "director":
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📝 Сұрақ Құрастыру",
                "🗑️ Сұрақтарды Басқару & Тексеру",
                "👥 Пайдаланушылар & Парольдерді Көру",
                "⚙️ Жеке Баптаулар (Пароль өзгерту)",
            ]
        )

        with tab1:
            selected_sub = st.selectbox(
                "Қай пәнге сұрақ құрастырасыз?:",
                list(st.session_state.questions.keys()),
            )
            q_type = st.selectbox(
                "Сұрақ түрін таңдаңыз:",
                ["Бір жауапты сұрақ", "Көп жауапты сұрақ (бірнеше дұрыс)"],
            )

            q_text = st.text_input("Сұрақтың мәтіні:")
            img_url = st.text_input("🖼️ Сурет сілтемесі (URL, міндетті емес):")

            st.write("Варианттар (A-F):")
            c1, c2 = st.columns(2)
            with c1:
                opt_a = st.text_input("A жауабы:")
                opt_b = st.text_input("B жауабы:")
                opt_c = st.text_input("C жауабы:")
            with c2:
                opt_d = st.text_input("D жауабы:")
                opt_e = st.text_input("E жауабы (міндетті емес):")
                opt_f = st.text_input("F жауабы (міндетті емес):")

            if q_type == "Бір жауапты сұрақ":
                correct_ans = st.radio(
                    "Дұрыс жауапты таңдаңыз:", ["A", "B", "C", "D", "E", "F"]
                )
                correct_selected = [correct_ans]
            else:
                st.write("Дұрыс жауаптарды белгілеңіз (бірнешеу):")
                ca, cb, cc = st.checkbox("A"), st.checkbox("B"), st.checkbox("C")
                cd, ce, cf = st.checkbox("D"), st.checkbox("E"), st.checkbox("F")
                correct_selected = []
                if ca:
                    correct_selected.append("A")
                if cb:
                    correct_selected.append("B")
                if cc:
                    correct_selected.append("C")
                if cd:
                    correct_selected.append("D")
                if ce:
                    correct_selected.append("E")
                if cf:
                    correct_selected.append("F")

            if st.button("Сұрақты Сақтау"):
                if not q_text or not (opt_a and opt_b and opt_c and opt_d):
                    st.error(
                        "⚠️ А, B, C, D варианттары мен сұрақ міндетті түрде толтырылуы тиіс!"
                    )
                elif len(correct_selected) == 0:
                    st.error("⚠️ Кемінде 1 дұрыс жауап көрсетілуі тиіс!")
                else:
                    st.session_state.questions[selected_sub].append(
                        {
                            "q": q_text,
                            "type": (
                                "single"
                                if q_type == "Бір жауапты сұрақ"
                                else "multi"
                            ),
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
                    st.success(
                        f"✅ '{selected_sub}' пәніне сұрақ сәтті қосылды!"
                    )

        with tab2:
            st.subheader(
                "🗑️ Сұрақтарды басқару, өшіру және бірден тексеріп көру"
            )
            del_sub = st.selectbox(
                "Пәнді таңдаңыз:",
                list(st.session_state.questions.keys()),
                key="del_sub_box",
            )
            q_list = st.session_state.questions[del_sub]

            if not q_list:
                st.info(f"ℹ️ '{del_sub}' пәнінде әлі сұрақтар жоқ.")
            else:
                for idx, q in enumerate(q_list):
                    st.markdown("---")
                    st.markdown(
                        f"**Сұрақ {idx+1}: {q['q']}** *(Түрі: {'Бір жауапты' if q['type']=='single' else 'Көп жауапты'})*"
                    )

                    opts = {k: v for k, v in q["options"].items() if v.strip()}
                    dir_ans = None

                    if q["type"] == "single":
                        formatted_opts = [f"{k}) {v}" for k, v in opts.items()]
                        chosen = st.radio(
                            "Жауапты таңдап көріңіз:",
                            formatted_opts,
                            key=f"dir_test_{del_sub}_{idx}",
                        )
                        dir_ans = [chosen[0]]
                    else:
                        st.write(
                            "Жауаптарды белгілеп тексеріңіз (бірнешеу):"
                        )
                        chosen_multi = []
                        for k, v in opts.items():
                            if st.checkbox(
                                f"{k}) {v}", key=f"dir_test_m_{del_sub}_{idx}_{k}"
                            ):
                                chosen_multi.append(k)
                        dir_ans = chosen_multi

                    col_chk, col_del = st.columns([1, 1])
                    with col_chk:
                        if st.button(
                            "⚡ Дұрыс/Қате тексеру",
                            key=f"check_btn_{del_sub}_{idx}",
                        ):
                            u_set = set(dir_ans)
                            c_set = set(q["correct"])
                            if u_set == c_set and len(u_set) > 0:
                                st.success(
                                    "✅ Дұрыс жауап! (Жауап дұрыс жұмыс істеп тұр)"
                                )
                            else:
                                st.error(
                                    f"❌ Қате! Дұрыс жауап(тар) мынау болуы тиіс: {', '.join(q['correct'])}"
                                )

                    with col_del:
                        if st.button(
                            "🗑️ Сұрақты өшіру", key=f"del_q_{del_sub}_{idx}"
                        ):
                            st.session_state.questions[del_sub].pop(idx)
                            st.success("🗑️ Сұрақ өшірілді!")
                            st.rerun()

        with tab3:
            st.subheader(
                "👥 Барлық Пайдаланушылар (Парольдерді көру және басқару)"
            )
            user_data_list = []
            for u_key, u_vals in st.session_state.users.items():
                user_data_list.append(
                    {
                        "Логин": u_key,
                        "Аты-жөні": u_vals.get("name", ""),
                        "Пароль": u_vals.get("pass", ""),
                        "Рөлі (Ранг)": u_vals.get("role", ""),
                        "Қалған доступ": u_vals.get("attempts", "-"),
                    }
                )

            st.dataframe(pd.DataFrame(user_data_list), use_container_width=True)

            st.write("---")
            st.subheader("➕ Жаңа Зам Директор немесе Оқушы Қосу")
            add_role = st.selectbox(
                "Қандай рөл қосасыз?", ["zam", "student"]
            )
            full_name_in = st.text_input("Толық аты-жөні:")
            login_in = st.text_input("Логин:")
            pass_in = st.text_input("Пароль:")
            attempts_in = st.number_input(
                "Бастапқы доступ саны (Оқушы үшін):",
                min_value=1,
                max_value=20,
                value=1,
            )

            if st.button("Пайдаланушыны Тіркеу"):
                if login_in and pass_in and full_name_in:
                    if login_in in st.session_state.users:
                        st.error("⚠️ Мұндай логин тіркеліп қойған!")
                    else:
                        st.session_state.users[login_in] = {
                            "name": full_name_in,
                            "pass": pass_in,
                            "role": add_role,
                            "fails": 0,
                            "ban_until": 0,
                            "attempts": attempts_in if add_role == "student" else 9999,
                        }
                        st.success(
                            f"✅ Жаңа {('Зам директор' if add_role=='zam' else 'Оқушы')} сәтті қосылды!"
                        )
                        st.rerun()
                else:
                    st.error("⚠️ Барлық өрістерді толтырыңыз!")

            st.write("---")
            st.subheader("🔑 Оқушыға Доступ (Минут) Беру")
            students = {
                k: v
                for k, v in st.session_state.users.items()
                if v["role"] == "student"
            }
            if not students:
                st.info("Тіркелген оқушылар жоқ.")
            else:
                st_target = st.selectbox(
                    "Оқушыны таңдаңыз:",
                    options=list(students.keys()),
                    format_func=lambda x: f"{students[x].get('name', x)} ({x})",
                )
                col_a, col_b, col_c = st.columns(3)
                if col_a.button("+1 Доступ беру"):
                    st.session_state.users[st_target]["attempts"] = (
                        st.session_state.users[st_target].get("attempts", 0) + 1
                    )
                    st.success("+1 доступ берілді!")
                    st.rerun()
                if col_b.button("+2 Доступ беру"):
                    st.session_state.users[st_target]["attempts"] = (
                        st.session_state.users[st_target].get("attempts", 0) + 2
                    )
                    st.success("+2 доступ берілді!")
                    st.rerun()
                if col_c.button("+3 Доступ беру"):
                    st.session_state.users[st_target]["attempts"] = (
                        st.session_state.users[st_target].get("attempts", 0) + 3
                    )
                    st.success("+3 доступ берілді!")
                    st.rerun()

        with tab4:
            st.subheader("⚙️ Директордың Жеке Баптаулары (Пароль өзгерту)")
            old_p = st.text_input("Ескі пароль:", type="password")
            new_p1 = st.text_input("Жаңа пароль:", type="password")
            new_p2 = st.text_input("Жаңа парольді қайталаңыз:", type="password")

            if st.button("Парольді Өзгерту"):
                curr_usr_obj = st.session_state.users[
                    st.session_state.logged_user
                ]
                if old_p != curr_usr_obj["pass"]:
                    st.error("❌ Ескі пароль қате енгізілді!")
                elif not new_p1 or new_p1 != new_p2:
                    st.error("❌ Жаңа парольдер сәйкес келмейді немесе бос!")
                else:
                    curr_usr_obj["pass"] = new_p1
                    st.success("✅ Пароль сәтті өзгертілді!")

    # --- ЗАМ ДИРЕКТОР ПАНЕЛІ ---
    if role == "zam":
        tab_z1, tab_z2 = st.tabs(
            [
                "📝 Сұрақ Құрастыру & Басқару",
                "👥 Оқушы Қосу & Доступ (Минут) Беру",
            ]
        )

        with tab_z1:
            st.subheader("🛠️ Зам Директор - Сұрақтарды басқару")
            selected_sub = st.selectbox(
                "Қай пәнге сұрақ құрастырасыз?:",
                list(st.session_state.questions.keys()),
                key="zam_sub",
            )
            q_type = st.selectbox(
                "Сұрақ түрін таңдаңыз:",
                ["Бір жауапты сұрақ", "Көп жауапты сұрақ (бірнеше дұрыс)"],
                key="zam_q_type",
            )

            q_text = st.text_input("Сұрақтың мәтіні:", key="zam_q_text")
            img_url = st.text_input(
                "🖼️ Сурет сілтемесі (URL, міндетті емес):", key="zam_img"
            )

            st.write("Варианттар (A-F):")
            c1, c2 = st.columns(2)
            with c1:
                opt_a = st.text_input("A жауабы:", key="zam_opt_a")
                opt_b = st.text_input("B жауабы:", key="zam_opt_b")
                opt_c = st.text_input("C жауабы:", key="zam_opt_c")
            with c2:
                opt_d = st.text_input("D жауабы:", key="zam_opt_d")
                opt_e = st.text_input("E жауабы (міндетті емес):", key="zam_opt_e")
                opt_f = st.text_input("F жауабы (міндетті емес):", key="zam_opt_f")

            if q_type == "Бір жауапты сұрақ":
                correct_ans = st.radio(
                    "Дұрыс жауапты таңдаңыз:",
                    ["A", "B", "C", "D", "E", "F"],
                    key="zam_corr_single",
                )
                correct_selected = [correct_ans]
            else:
                st.write("Дұрыс жауаптарды белгілеңіз (бірнешеу):")
                ca, cb, cc = (
                    st.checkbox("A", key="z_ca"),
                    st.checkbox("B", key="z_cb"),
                    st.checkbox("C", key="z_cc"),
                )
                cd, ce, cf = (
                    st.checkbox("D", key="z_cd"),
                    st.checkbox("E", key="z_ce"),
                    st.checkbox("F", key="z_cf"),
                )
                correct_selected = []
                if ca:
                    correct_selected.append("A")
                if cb:
                    correct_selected.append("B")
                if cc:
                    correct_selected.append("C")
                if cd:
                    correct_selected.append("D")
                if ce:
                    correct_selected.append("E")
                if cf:
                    correct_selected.append("F")

            if st.button("Сұрақты Сақтау (Зам)"):
                if not q_text or not (opt_a and opt_b and opt_c and opt_d):
                    st.error("⚠️ А, B, C, D варианттары мен сұрақ толтырылуы тиіс!")
                elif len(correct_selected) == 0:
                    st.error("⚠️ Кемінде 1 дұрыс жауап көрсетілуі тиіс!")
                else:
                    st.session_state.questions[selected_sub].append(
                        {
                            "q": q_text,
                            "type": (
                                "single"
                                if q_type == "Бір жауапты сұрақ"
                                else "multi"
                            ),
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
                    st.success(f"✅ '{selected_sub}' пәніне сұрақ сәтті қосылды!")

        with tab_z2:
            st.subheader("👥 Жаңа Оқушы Қосу")
            new_st_u_z = st.text_input("Оқушының логині:", key="z_st_u")
            new_st_p_z = st.text_input("Оқушының паролі:", key="z_st_p")
            new_st_name_z = st.text_input(
                "Оқушының толық аты-жөні:", key="z_st_name"
            )
            init_att_z = st.number_input(
                "Бастапқы доступ саны:",
                min_value=1,
                max_value=10,
                value=1,
                key="z_st_att",
            )

            if st.button("Оқушыны Тіркеу (Зам)", key="z_reg_btn"):
                if new_st_u_z and new_st_p_z and new_st_name_z:
                    if new_st_u_z in st.session_state.users:
                        st.error("⚠️ Мұндай логин бар!")
                    else:
                        st.session_state.users[new_st_u_z] = {
                            "name": new_st_name_z,
                            "pass": new_st_p_z,
                            "role": "student",
                            "fails": 0,
                            "ban_until": 0,
                            "attempts": init_att_z,
                        }
                        st.success("✅ Оқушы сәтті қосылды!")
                        st.rerun()
                else:
                    st.error("⚠️ Өрістерді толық толтырыңыз!")

            st.write("---")
            st.subheader("🔑 Оқушыға Доступ (Минут) Беру")
            students = {
                k: v
                for k, v in st.session_state.users.items()
                if v["role"] == "student"
            }
            if not students:
                st.info("Тіркелген оқушылар жоқ.")
            else:
                st_target_z = st.selectbox(
                    "Оқушыны таңдаңыз:",
                    options=list(students.keys()),
                    format_func=lambda x: f"{students[x].get('name', x)} ({x})",
                    key="z_st_sel",
                )
                col_a, col_b, col_c = st.columns(3)
                if col_a.button("+1 Доступ беру", key="z_btn_1"):
                    st.session_state.users[st_target_z]["attempts"] = (
                        st.session_state.users[st_target_z].get("attempts", 0)
                        + 1
                    )
                    st.success("+1 доступ берілді!")
                    st.rerun()
                if col_b.button("+2 Доступ беру", key="z_btn_2"):
                    st.session_state.users[st_target_z]["attempts"] = (
                        st.session_state.users[st_target_z].get("attempts", 0)
                        + 2
                    )
                    st.success("+2 доступ берілді!")
                    st.rerun()
                if col_c.button("+3 Доступ беру", key="z_btn_3"):
                    st.session_state.users[st_target_z]["attempts"] = (
                        st.session_state.users[st_target_z].get("attempts", 0)
                        + 3
                    )
                    st.success("+3 доступ берілді!")
                    st.rerun()

    # --- ОҚУШЫ ТЕСТІ ЖӘНЕ СЕРТИФИКАТ ---
    if role == "student":
        if st.session_state.last_cert:
            cert = st.session_state.last_cert

            st.markdown(
                f"""
            <div class="certificate-box">
                <div class="cert-title">🏆 CERTIFICATE OF ACHIEVEMENT 🏆</div>
                <div class="cert-academy">KASUM AHMAD TEST ACADEMY</div>
                <p class="cert-body">Осы сертификат табысты түрде тест тапсырған оқушыға беріледі:</p>
                <div class="cert-name">{cert['user_fullname']}</div>
                <br>
                <p class="cert-body">Пән: <b>{cert['subject']}</b></p>
                <div class="cert-score">{cert['score']}</div>
                <p class="cert-body">Жалпы нәтиже: <b>{cert['percentage']}%</b></p>
                <div class="cert-rank">🥇 Рейтингтегі орны: {cert['rank']}-орын (Жалпы {cert['total_students']} оқушының ішінен)</div>
                <div class="cert-footer">
                    <div>📅 Күні: {cert['date']}</div>
                    <div>✍️ Тексерілді</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            if st.session_state.review_result:
                st.subheader("📋 Сіздің жауаптарыңыз бен талдау:")
                for item in st.session_state.review_result:
                    color = "#00FF66" if item["is_correct"] else "#FF4B4B"
                    status_text = "✅ Дұрыс" if item["is_correct"] else "❌ Қате"
                    st.markdown(
                        f"""
                    <div style="background:#131722; padding:15px; border-radius:8px; border-left:5px solid {color}; margin-bottom:10px;">
                        <p style="margin:0; font-size:18px;"><b>{item['q_num']}. {item['question']}</b></p>
                        <p style="margin:5px 0 0 0;">Сіздің жауабыңыз: <code>{', '.join(item['user_ans']) if item['user_ans'] else 'Бос'}</code> | Дұрыс жауап: <code>{', '.join(item['correct_ans'])}</code> - <b style="color:{color};">{status_text}</b></p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                st.info("ℹ️ Нәтиже жүйеге сақталды.")
            with col_btn2:
                if st.button("🚪 Жүйеден шығу (Logout)"):
                    st.session_state.logged_user = None
                    st.session_state.last_cert = None
                    st.session_state.review_result = None
                    st.session_state.selected_exam_subject = None
                    st.rerun()

        else:
            if not st.session_state.selected_exam_subject:
                st.subheader("🎯 Қай пәнді тапсырасыз?")
                st.write(
                    "Төмендегі тізімнен тек **1 пәнді** таңдап, тестті бастаңыз:"
                )

                chosen_sub = st.selectbox(
                    "Пәнді таңдаңыз:",
                    list(st.session_state.questions.keys()),
                )

                if st.button("🚀 Таңдалған пән бойынша тестті бастау"):
                    st.session_state.selected_exam_subject = chosen_sub
                    st.rerun()
            else:
                subject = st.session_state.selected_exam_subject
                q_list = st.session_state.questions[subject]

                st.markdown(f"### 📚 Тапсырылып жатқан пән: `{subject}`")

                if not q_list:
                    st.warning(
                        f"⚠️ Бұл пәнге әлі сұрақтар қосылмаған! Директордың немесе Замның сұрақ қосуын күтіңіз."
                    )
                    if st.button("🔄 Басқа пән таңдау"):
                        st.session_state.selected_exam_subject = None
                        st.rerun()
                else:
                    user_answers = {}
                    for i, q in enumerate(q_list):
                        st.markdown(
                            f"""
                        <div class="question-box">
                            <h4>❓ {i+1}-сұрақ: {q['q']}</h4>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        if q.get("image"):
                            st.image(q["image"], use_column_width=True)

                        opts = {
                            k: v for k, v in q["options"].items() if v.strip()
                        }

                        if q["type"] == "single":
                            formatted = [f"{k}) {v}" for k, v in opts.items()]
                            ans = st.radio(
                                "Жауапты таңдаңыз:",
                                formatted,
                                key=f"q_{subject}_{i}",
                            )
                            user_answers[i] = [ans[0]]
                        else:
                            st.write(
                                "Көп жауапты тест (бірнеше дұрыс жауапты белгілеңіз):"
                            )
                            selected = []
                            for k, v in opts.items():
                                if st.checkbox(
                                    f"{k}) {v}", key=f"q_{subject}_{i}_{k}"
                                ):
                                    selected.append(k)
                            user_answers[i] = selected

                        st.markdown("<br>", unsafe_allow_html=True)

                    if st.button("🚀 Тестті Аяқтау және Нәтижені Көру"):
                        score = 0
                        step_scores = []
                        review_data = []

                        for i, q in enumerate(q_list):
                            u_ans = set(user_answers.get(i, []))
                            c_ans = set(q["correct"])
                            is_corr = u_ans == c_ans and len(u_ans) > 0

                            if is_corr:
                                score += 1
                                step_scores.append(1)
                            else:
                                step_scores.append(-1)

                            review_data.append(
                                {
                                    "q_num": i + 1,
                                    "question": q["q"],
                                    "user_ans": list(u_ans),
                                    "correct_ans": list(c_ans),
                                    "is_correct": is_corr,
                                }
                            )

                        total_q = len(q_list)
                        percentage = round((score / total_q) * 100, 1)
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

                        st.session_state.results.append(
                            {
                                "user": st.session_state.logged_user,
                                "user_name": full_name,
                                "subject": subject,
                                "time": now_str,
                                "score": f"{score}/{total_q}",
                                "raw_score": score,
                                "step_scores": step_scores,
                            }
                        )

                        sub_results = [
                            r
                            for r in st.session_state.results
                            if r["subject"] == subject
                        ]
                        best_scores = {}
                        for r in sub_results:
                            u = r["user"]
                            if (
                                u not in best_scores
                                or r["raw_score"] > best_scores[u]
                            ):
                                best_scores[u] = r["raw_score"]

                        sorted_rank = sorted(
                            best_scores.items(), key=lambda x: x[1], reverse=True
                        )
                        rank = 1
                        for idx, (u, sc) in enumerate(sorted_rank):
                            if u == st.session_state.logged_user:
                                rank = idx + 1
                                break

                        total_students = len(best_scores)

                        st.session_state.users[st.session_state.logged_user][
                            "attempts"
                        ] -= 1

                        st.session_state.last_cert = {
                            "user_fullname": full_name,
                            "subject": subject,
                            "score": f"{score} / {total_q}",
                            "percentage": percentage,
                            "rank": rank,
                            "total_students": total_students,
                            "date": now_str,
                        }

                        st.session_state.review_result = review_data
                        st.rerun()
