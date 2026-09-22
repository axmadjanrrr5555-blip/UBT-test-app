from datetime import datetime
import time
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="KASUM AHMAD - TRADING TEST", layout="wide")

# TRADINGVIEW / BINANCE DARK STYLE CSS
st.markdown(
    """
    <style>
    /* Негізгі фон - Трейдинг күңгірт фоны */
    .stApp {
        background-color: #0b0e14 !important;
        background-image: radial-gradient(circle at 50% 20%, #131722 0%, #0b0e14 100%);
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
    }
    
    /* Неонды Тақырыптар */
    .main-title {
        font-size: 70px;
        font-weight: 900;
        letter-spacing: 6px;
        color: #00FF66 !important;
        margin-bottom: 0px;
        line-height: 1;
        text-shadow: 0 0 20px rgba(0, 255, 102, 0.5);
    }
    
    .sub-title {
        font-size: 70px;
        font-weight: 900;
        letter-spacing: 6px;
        color: #00FF66 !important;
        text-align: right;
        margin-top: 0px;
        line-height: 1;
        text-shadow: 0 0 20px rgba(0, 255, 102, 0.5);
    }

    /* Мәтіндер мен тақырыпшалар */
    h1, h2, h3, h4, h5, h6, p, label, div, span, small, li { 
        color: #D1D4DC !important; 
        font-weight: 600 !important;
    }
    
    /* Терминал стильді карточкалар */
    div[data-testid="stMetricValue"] {
        color: #00FF66 !important;
        font-size: 32px !important;
        font-weight: bold;
    }

    /* Батырмалар - Trading Order Button */
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

    /* Енгізу өрістері (Input / Selectbox) */
    .stTextInput>div>div>input, .stSelectbox>div>div {
        color: #00FF66 !important;
        background-color: #1e222d !important;
        border: 1px solid #2a2e39 !important;
        border-radius: 6px;
    }

    /* Табтарды әрлеу */
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
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">KASUM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AHMAD</div>', unsafe_allow_html=True)
st.write("---")

# Session State баптаулары
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

# --- КІРУ БОЛЫМЫ ---
if not st.session_state.logged_user:
    st.subheader("🔑 Trading Terminal Login")
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
    st.sidebar.markdown(f"📈 **Терминал:** `{st.session_state.logged_user}`")
    st.sidebar.markdown(f"🏷️ **Статус:** `<span style='color:#00FF66'>{role.upper()}</span>`", unsafe_allow_html=True)
    
    if st.sidebar.button("Шығу / Logout"):
        st.session_state.logged_user = None
        st.rerun()

    # --- ДИРЕКТОР ПАНЕЛІ ---
    if role == "director":
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "🖥️ Кіру Тарихы",
                "🔑 Аккаунттар",
                "📊 Нәтижелер",
                "🔓 Банды Шешу",
                "🔐 Доступ Реттеу",
            ]
        )

        with tab1:
            for log in reversed(st.session_state.login_logs):
                st.write(
                    f"⏱️ `{log['time']}` | 👤 User: **{log['user']}** ({log['role']})"
                )

        with tab2:
            st.json(st.session_state.users)

        with tab3:
            for r in st.session_state.results:
                st.write(
                    f"📈 **{r['user']}** | 📚 {r['subject']} | 🕒 {r['time']} | 🎯 Балл: `{r['score']}`"
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
                "Зам директорға сұрақ қосуға рұқсат",
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
                    st.success("Пароль ауыстырылды!")

            new_zam_p = st.text_input(
                "Жаңа Зам паролі:", type="password", key="np_zam"
            )
            if st.button("Зам паролін жаңарту"):
                if new_zam_p.strip():
                    st.session_state.users["zam"]["pass"] = new_zam_p.strip()
                    st.success("Пароль ауыстырылды!")

    # --- СҰРАҚ ҚОСУ (ДИРЕКТОР / ЗАМ) ---
    if role in ["director", "zam"]:
        st.subheader("⚙️ Сұрақтарды басқару")
        z_tab1, z_tab2 = st.tabs(["📝 Сұрақ Құрастыру", "👤 Оқушы Қосу"])

        with z_tab1:
            if role == "zam" and not st.session_state.can_zam_add_q:
                st.error("⛔ Сұрақ қосуға доступ жабық!")
            else:
                selected_sub = st.selectbox(
                    "Пән таңдаңыз:", list(st.session_state.questions.keys())
                )
                q_text = st.text_input("Сұрақтың матні:")
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

                st.write("Дұрыс жауаптар (макс 3):")
                ca, cb, cc = st.checkbox("A"), st.checkbox("B"), st.checkbox("C")
                cd, ce, cf = st.checkbox("D"), st.checkbox("E"), st.checkbox("F")

                correct_selected = []
                if ca: correct_selected.append("A")
                if cb: correct_selected.append("B")
                if cc: correct_selected.append("C")
                if cd: correct_selected.append("D")
                if ce: correct_selected.append("E")
                if cf: correct_selected.append("F")

                if st.button("Сұрақты Сақтау"):
                    has_extra = bool(opt_e.strip() or opt_f.strip())
                    if not q_text or not (opt_a and opt_b and opt_c and opt_d):
                        st.error("⚠️ А, B, C, D варианттары мен сұрақ толтырылуы тиіс!")
                    elif len(correct_selected) == 0:
                        st.error("⚠️ Кемінде 1 дұрыс жауап белгілеңіз!")
                    elif len(correct_selected) > 3:
                        st.error("⚠️ 3-тен артық дұрыс жауап таңдауға болмайды!")
                    elif not has_extra and len(correct_selected) > 1:
                        st.error("⚠️ 4 вариантты тестіде тек 1 дұрыс жауап болуы керек!")
                    else:
                        st.session_state.questions[selected_sub].append(
                            {
                                "q": q_text,
                                "options": {
                                    "A": opt_a, "B": opt_b, "C": opt_c,
                                    "D": opt_d, "E": opt_e, "F": opt_f,
                                },
                                "correct": correct_selected,
                                "image": img_url.strip(),
                            }
                        )
                        st.success("✅ Сұрақ сақталды!")

        with z_tab2:
            new_st_u = st.text_input("Оқушы логині:")
            new_st_p = st.text_input("Оқушы паролі:")
            if st.button("Оқушыны Тіркеу"):
                if new_st_u and new_st_p:
                    st.session_state.users[new_st_u] = {
                        "pass": new_st_p,
                        "role": "student",
                        "fails": 0,
                        "ban_until": 0,
                    }
                    st.success("Оқушы сәтті қосылды!")

    # --- ОҚУШЫ ТЕСТІ ЖӘНЕ ТРЕЙДИНГ ГРАФИГІ ---
    if role == "student":
        subject = st.selectbox("Пән таңдаңыз:", list(st.session_state.questions.keys()))
        q_list = st.session_state.questions[subject]

        if q_list:
            user_answers = {}
            for i, q in enumerate(q_list):
                st.markdown(f"#### ❓ {i+1}-сұрақ: {q['q']}")
                if q.get("image"):
                    st.image(q["image"], use_column_width=True)

                opts = {k: v for k, v in q["options"].items() if v.strip()}

                # 1 дұрыс жауап немесе 4 вариант -> Radio Button
                if len(opts) <= 4 or len(q["correct"]) == 1:
                    formatted = [f"{k}) {v}" for k, v in opts.items()]
                    ans = st.radio("Жауапты таңдаңыз:", formatted, key=f"q_{subject}_{i}")
                    user_answers[i] = [ans[0]]
                else:
                    st.write("Көп жауапты тест (бірнешеуін белгілеңіз):")
                    selected = []
                    for k, v in opts.items():
                        if st.checkbox(f"{k}) {v}", key=f"q_{subject}_{i}_{k}"):
                            selected.append(k)
                    user_answers[i] = selected

            if st.button("🚀 Тестті Тапсыру (Trading Analysis)"):
                score = 0
                step_scores = []
                
                for i, q in enumerate(q_list):
                    u_ans = set(user_answers.get(i, []))
                    c_ans = set(q["correct"])
                    if u_ans == c_ans and len(u_ans) > 0:
                        score += 1
                        step_scores.append(1)  # Дұрыс - жасыл тренд
                    else:
                        step_scores.append(-1) # Қате - қызыл тренд

                wrong_score = len(q_list) - score
                st.session_state.results.append({
                    "user": st.session_state.logged_user,
                    "subject": subject,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "score": f"{score}/{len(q_list)}",
                })

                st.write("---")
                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("🎯 Жалпы Балл", f"{score} / {len(q_list)}")
                col_m2.metric("🟢 Дұрыс (Long)", f"{score}")
                col_m3.metric("🔴 Қате (Short)", f"{wrong_score}")

                # --- TRADING STYLE CANDLESTICK / AREA CHART ---
                st.subheader("📈 Трейдингтік Динамика Графигі (Trading Chart)")

                cumulative_profit = [0]
                curr = 0
                for s in step_scores:
                    curr += s
                    cumulative_profit.append(curr)

                # Trading Chart құрастыру (Plotly)
                fig = go.Figure()

                # Неонды график сызығы
                fig.add_trace(go.Scatter(
                    x=list(range(len(cumulative_profit))),
                    y=cumulative_profit,
                    mode='lines+markers',
                    name='Балл Тренді',
                    line=dict(color='#00FF66' if score >= wrong_score else '#FF3366', width=3),
                    marker=dict(size=8, color='#00FF66' if score >= wrong_score else '#FF3366'),
                    fill='tozeroy',
                    fillcolor='rgba(0, 255, 102, 0.1)' if score >= wrong_score else 'rgba(255, 51, 102, 0.1)'
                ))

                # Свечалар / Дұрыс-Қате индикаторлары
                fig.add_trace(go.Bar(
                    x=list(range(1, len(step_scores) + 1)),
                    y=[1 if x == 1 else -1 for x in step_scores],
                    marker_color=['#00FF66' if x == 1 else '#FF3366' for x in step_scores],
                    name='Сұрақ нәтижесі'
                ))

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#0b0e14",
                    plot_bgcolor="#131722",
                    title="Сұрақтар бойынша трендтік талдау (TradingView Style)",
                    xaxis=dict(title="Сұрақ номері", showgrid=True, gridcolor='#1e222d'),
                    yaxis=dict(title="Профит / Балл", showgrid=True, gridcolor='#1e222d'),
                    font=dict(color="#D1D4DC")
                )

                st.plotly_chart(fig, use_container_width=True)
