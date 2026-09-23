from datetime import datetime
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ONLINE TEST SYSTEM", layout="wide", page_icon="📜"
)

# TRADINGVIEW / BINANCE DARK STYLE CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14 !important;
        background-image: radial-gradient(circle at 50% 20%, #131722 0%, #0b0e14 100%);
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
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
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #131722;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #848e9c !important;
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

# Session State баптаулары
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

if "last_cert" not in st.session_state:
    st.session_state.last_cert = None

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
                    st.error(f"⛔ Блокталғансыз! {left} мин қалды.")
                elif usr["pass"] == password:
                    if usr["role"] == "student" and usr.get("attempts", 0) <= 0:
                        st.error(
                            "⛔ Сізде тест тапсыруға доступ жоқ! Директор немесе Зам-нан рұқсат сұраңыз."
                        )
                    else:
                        usr["fails"] = 0
                        st.session_state.logged_user = login
                        st.session_state.last_cert = None
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
                    if usr["fails"] >= 5:
                        usr["ban_until"] = curr_time + 1800
                        st.error("⛔ 5 рет қате кірілді! 30 мин БАН.")
                    else:
                        st.error(
                            f"❌ Қате пароль! Қалған мүмкіндік: {5 - usr['fails']}"
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

    if st.sidebar.button("Шығу / Logout"):
        st.session_state.logged_user = None
        st.session_state.last_cert = None
        st.rerun()

    # --- ДИРЕКТОР ПАНЕЛІ ---
    if role == "director":
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "📊 Оқушылар Графигі",
                "🔑 Доступ/Мүмкіндік Беру",
                "🖥️ Кіру Тарихы",
                "📋 Тест Нәтижелері",
                "🔓 Банды Шешу",
                "🔐 Доступ Реттеу",
            ]
        )

        with tab1:
            st.subheader("📈 Оқушылардың графиктерін қарау")
            if not st.session_state.results:
                st.info("ℹ️ Әлі ешқандай оқушы тест тапсырмады.")
            else:
                student_list = list(
                    set(r["user_name"] for r in st.session_state.results)
                )
                selected_student = st.selectbox(
                    "Оқушыны таңдаңыз:", student_list
                )

                student_results = [
                    r
                    for r in st.session_state.results
                    if r["user_name"] == selected_student
                ]

                st.write(
                    f"**{selected_student}** оқушысының тапсырған тесттері ({len(student_results)} рет):"
                )

                for idx, res in enumerate(reversed(student_results)):
                    st.markdown(
                        f"--- \n 🕒 **Уақыты:** {res['time']} | 📚 **Пән:** {res['subject']} | 🎯 **Балл:** `{res['score']}`"
                    )

                    cumulative_profit = [0]
                    curr = 0
                    for s in res["step_scores"]:
                        curr += s
                        cumulative_profit.append(curr)

                    st.line_chart(
                        pd.DataFrame({"Балл тренді": cumulative_profit})
                    )

        with tab2:
            st.subheader("🔑 Оқушыларға тест тапсыруға доступ беру")
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
                st.write(
                    f"Қазіргі қолжетімді тапсыру мүмкіндігі: **{st.session_state.users[st_target].get('attempts', 0)}** рет."
                )

                col_a, col_b, col_c = st.columns(3)
                if col_a.button("+1 Доступ беру"):
                    st.session_state.users[st_target]["attempts"] = (
                        st.session_state.users[st_target].get("attempts", 0) + 1
                    )
                    st.success(f"+1 доступ берілді!")
                    st.rerun()

                if col_b.button("+2 Доступ беру"):
                    st.session_state.users[st_target]["attempts"] = (
                        st.session_state.users[st_target].get("attempts", 0) + 2
                    )
                    st.success(f"+2 доступ берілді!")
                    st.rerun()

                if col_c.button("+3 Доступ беру"):
                    st.session_state.users[st_target]["attempts"] = (
                        st.session_state.users[st_target].get("attempts", 0) + 3
                    )
                    st.success(f"+3 доступ берілді!")
                    st.rerun()

        with tab3:
            for log in reversed(st.session_state.login_logs):
                st.write(
                    f"⏱️ `{log['time']}` | 👤 User: **{log['user']}** (`{log['username']}`) - {log['role']}"
                )

        with tab4:
            for r in st.session_state.results:
                st.write(
                    f"📈 **{r['user_name']}** | 📚 {r['subject']} | 🕒 {r['time']} | 🎯 Балл: `{r['score']}`"
                )

        with tab5:
            for u_name, u_data in st.session_state.users.items():
                if u_data["ban_until"] > curr_time:
                    if st.button(
                        f"Unban: {u_data.get('name', u_name)} ({u_name})"
                    ):
                        u_data["ban_until"] = 0
                        u_data["fails"] = 0
                        st.success("Баннан шығарылды!")
                        st.rerun()

        with tab6:
            allow_zam = st.checkbox(
                "Зам директорға сұрақ қосуға рұқсат",
                value=st.session_state.can_zam_add_q,
            )
            st.session_state.can_zam_add_q = allow_zam

            dir_new_name = st.text_input(
                "Директордың Аты-Жөні:",
                value=st.session_state.users["director"].get("name", ""),
            )
            new_dir_p = st.text_input(
                "Жаңа Директор паролі:", type="password", key="np_dir"
            )
            if st.button("Директор деректерін жаңарту"):
                st.session_state.users["director"]["name"] = dir_new_name
                if new_dir_p.strip():
                    st.session_state.users["director"]["pass"] = (
                        new_dir_p.strip()
                    )
                st.success("Деректер сақталды!")
                st.rerun()

            zam_new_name = st.text_input(
                "Замның Аты-Жөні:",
                value=st.session_state.users["zam"].get("name", ""),
            )
            new_zam_p = st.text_input(
                "Жаңа Зам паролі:", type="password", key="np_zam"
            )
            if st.button("Зам деректерін жаңарту"):
                st.session_state.users["zam"]["name"] = zam_new_name
                if new_zam_p.strip():
                    st.session_state.users["zam"]["pass"] = new_zam_p.strip()
                st.success("Деректер сақталды!")
                st.rerun()

    # --- СҰРАҚ ҚОСУ ЖӘНЕ ОҚУШЫҒА ДОСТУП БЕРУ (ЗАМ/ДИРЕКТОР) ---
    if role in ["director", "zam"]:
        st.subheader("⚙️ Сұрақтар мен Оқушыларды басқару")
        z_tab1, z_tab2 = st.tabs(["📝 Сұрақ Құрастыру", "👤 Оқушы Тіркеу / Доступ"])

        with z_tab1:
            if role == "zam" and not st.session_state.can_zam_add_q:
                st.error("⛔ Сұрақ қосуға доступ жабық!")
            else:
                selected_sub = st.selectbox(
                    "Пән таңдаңыз:", list(st.session_state.questions.keys())
                )
                q_text = st.text_input("Сұрақтың мәтіні:")
                img_url = st.text_input(
                    "🖼️ Сурет сілтемесі (URL, міндетті емес):"
                )

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

                st.write("Дұрыс жауаптар (макс 3):")
                ca, cb, cc = (
                    st.checkbox("A"),
                    st.checkbox("B"),
                    st.checkbox("C"),
                )
                cd, ce, cf = (
                    st.checkbox("D"),
                    st.checkbox("E"),
                    st.checkbox("F"),
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

                if st.button("Сұрақты Сақтау"):
                    has_extra = bool(opt_e.strip() or opt_f.strip())
                    if not q_text or not (opt_a and opt_b and opt_c and opt_d):
                        st.error(
                            "⚠️ А, B, C, D варианттары мен сұрақ толтырылуы тиіс!"
                        )
                    elif len(correct_selected) == 0:
                        st.error("⚠️ Кемінде 1 дұрыс жауап белгілеңіз!")
                    elif len(correct_selected) > 3:
                        st.error(
                            "⚠️ 3-тен артық дұрыс жауап таңдауға болмайды!"
                        )
                    elif not has_extra and len(correct_selected) > 1:
                        st.error(
                            "⚠️ 4 вариантты тестіде тек 1 дұрыс жауап болуы керек!"
                        )
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
                        st.success("✅ Сұрақ сақталды!")

        with z_tab2:
            st_fullname = st.text_input("Оқушының Толық Аты-Жөні:")
            new_st_u = st.text_input("Оқушы логині:")
            new_st_p = st.text_input("Оқушы паролі:")
            init_attempts = st.number_input(
                "Бастапқы доступ саны:", min_value=1, max_value=10, value=1
            )
            if st.button("Оқушыны Тіркеу"):
                if new_st_u and new_st_p and st_fullname:
                    st.session_state.users[new_st_u] = {
                        "name": st_fullname,
                        "pass": new_st_p,
                        "role": "student",
                        "fails": 0,
                        "ban_until": 0,
                        "attempts": init_attempts,
                    }
                    st.success("Оқушы сәтті қосылды!")
                else:
                    st.error("⚠️ Барлық өрістерді толтырыңыз!")

    # --- ОҚУШЫ ТЕСТІ ЖӘНЕ СЕРТИФИКАТ ---
    if role == "student":
        if st.session_state.last_cert:
            cert = st.session_state.last_cert

            # Сертификат: "KASUM AHMAD TEST ACADEMY" деп өзгертілді
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

            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                st.info("ℹ️ Нәтиже жүйеге сақталды.")
            with col_btn2:
                if st.button("🚪 Жүйеден шығу (Logout)"):
                    st.session_state.logged_user = None
                    st.session_state.last_cert = None
                    st.rerun()

        else:
            subject = st.selectbox(
                "Пән таңдаңыз:", list(st.session_state.questions.keys())
            )
            q_list = st.session_state.questions[subject]

            if q_list:
                user_answers = {}
                for i, q in enumerate(q_list):
                    st.markdown(f"#### ❓ {i+1}-сұрақ: {q['q']}")
                    if q.get("image"):
                        st.image(q["image"], use_column_width=True)

                    opts = {k: v for k, v in q["options"].items() if v.strip()}

                    if len(opts) <= 4 or len(q["correct"]) == 1:
                        formatted = [f"{k}) {v}" for k, v in opts.items()]
                        ans = st.radio(
                            "Жауапты таңдаңыз:",
                            formatted,
                            key=f"q_{subject}_{i}",
                        )
                        user_answers[i] = [ans[0]]
                    else:
                        st.write("Көп жауапты тест (бірнешеуін белгілеңіз):")
                        selected = []
                        for k, v in opts.items():
                            if st.checkbox(
                                f"{k}) {v}", key=f"q_{subject}_{i}_{k}"
                            ):
                                selected.append(k)
                        user_answers[i] = selected

                if st.button("🚀 Тестті Аяқтау және Сертификат Алу"):
                    score = 0
                    step_scores = []

                    for i, q in enumerate(q_list):
                        u_ans = set(user_answers.get(i, []))
                        c_ans = set(q["correct"])
                        if u_ans == c_ans and len(u_ans) > 0:
                            score += 1
                            step_scores.append(1)
                        else:
                            step_scores.append(-1)

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

                    st.rerun()
