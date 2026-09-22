import time
from datetime import datetime
import streamlit as st
import base64


# =========================================================
# БЕТТІ БАПТАУ
# =========================================================

st.set_page_config(
    page_title="KASUM AHMAD",
    layout="wide"
)


# =========================================================
# ФОН
# =========================================================

with open("background.jpg", "rb") as f:
    bg = base64.b64encode(f.read()).decode()


# =========================================================
# ДИЗАЙН / CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       SIDEBAR ЖАСЫРУ
       ===================================================== */

    [data-testid="stSidebar"] {{
        display: none !important;
    }}

    [data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}


    /* =====================================================
       STREAMLIT ЖОҒАРҒЫ ПАНЕЛІ
       ===================================================== */

    header {{
        background: transparent !important;
    }}


    /* =====================================================
       НЕГІЗГІ ФОН
       ===================================================== */

    .stApp {{
        background-image:
            linear-gradient(
                rgba(3, 18, 35, 0.55),
                rgba(3, 18, 35, 0.70)
            ),
            url("data:image/jpeg;base64,{bg}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}


    /* =====================================================
       НЕГІЗГІ КОНТЕНТ
       ===================================================== */

    .block-container {{
        max-width: 1100px !important;

        padding-top: 100px !important;
        padding-bottom: 50px !important;
    }}


    /* =====================================================
       KASUM
       ===================================================== */

    .main-title {{
        font-size: 80px;

        font-weight: 900;

        letter-spacing: 6px;

        color: white !important;

        line-height: 1;

        margin-top: 0px;
        margin-bottom: 10px;

        text-shadow:
            0 0 20px rgba(255,255,255,0.35);

        position: relative;

        z-index: 10;
    }}


    /* =====================================================
       AHMAD
       ===================================================== */

    .sub-title {{
        font-size: 80px;

        font-weight: 900;

        letter-spacing: 6px;

        color: white !important;

        text-align: right;

        line-height: 1;

        margin-top: 0px;

        text-shadow:
            0 0 20px rgba(255,255,255,0.35);

        position: relative;

        z-index: 10;
    }}


    /* =====================================================
       БАРЛЫҚ МӘТІН
       ===================================================== */

    h1, h2, h3, h4, h5, h6,
    p, label, div, span {{
        color: white !important;
    }}


    /* =====================================================
       INPUT
       ===================================================== */

    .stTextInput input {{
        background-color:
            rgba(20, 40, 60, 0.65) !important;

        color: white !important;

        border:
            1px solid rgba(255,255,255,0.45) !important;

        border-radius: 8px !important;

        height: 50px;
    }}


    .stTextInput input::placeholder {{
        color:
            rgba(255,255,255,0.65) !important;
    }}


    /* =====================================================
       БАТЫРМАЛАР
       ===================================================== */

    .stButton > button {{
        width: 100%;

        height: 50px;

        background-color:
            rgba(5, 20, 35, 0.70) !important;

        color: white !important;

        border:
            1px solid rgba(255,255,255,0.75) !important;

        border-radius: 8px !important;

        font-size: 18px;

        font-weight: 600;

        transition: 0.3s;
    }}


    .stButton > button:hover {{
        background-color:
            rgba(255,255,255,0.15) !important;

        border-color: white !important;
    }}


    /* =====================================================
       ШЫҒУ БАТЫРМАСЫ
       ===================================================== */

    .logout-area {{
        margin-top: -40px;
        margin-bottom: 20px;
    }}


    /* =====================================================
       КІРУ ТАҚЫРЫБЫ
       ===================================================== */

    .login-title {{
        font-size: 25px;

        font-weight: 700;

        margin-bottom: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KASUM AHMAD
# =========================================================

st.markdown(
    '<div class="main-title">KASUM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AHMAD</div>',
    unsafe_allow_html=True
)

st.write("---")


# =========================================================
# БАЗАНЫ БАПТАУ
# =========================================================

if "users" not in st.session_state:

    st.session_state.users = {

        "director": {
            "pass": "dir123",
            "role": "director",
            "fails": 0,
            "ban_until": 0,
        },

        "zam": {
            "pass": "zam123",
            "role": "zam",
            "fails": 0,
            "ban_until": 0
        },

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


# =========================================================
# КІРУ БӨЛІМІ
# =========================================================

if not st.session_state.logged_user:

    st.markdown(
        '<div class="login-title">🔑 Кіру</div>',
        unsafe_allow_html=True
    )


    login = st.text_input(
        "Логин:",
        placeholder="Логин енгізіңіз..."
    )


    password = st.text_input(
        "Пароль:",
        type="password",
        placeholder="Пароль енгізіңіз..."
    )


    if st.button("Кіру"):

        if login in st.session_state.users:

            usr = st.session_state.users[login]


            # =================================================
            # БАН ТЕКСЕРУ
            # =================================================

            if usr["ban_until"] > curr_time:

                left = int(
                    (usr["ban_until"] - curr_time) // 60
                )

                st.error(
                    f"⛔ Блокталғансыз! {left} мин қалды."
                )


            # =================================================
            # ПАРОЛЬ ДҰРЫС
            # =================================================

            elif usr["pass"] == password:

                usr["fails"] = 0

                st.session_state.logged_user = login


                login_time = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                st.session_state.login_logs.append(
                    {
                        "user": login,
                        "time": login_time,
                        "role": usr["role"]
                    }
                )


                st.rerun()


            # =================================================
            # ПАРОЛЬ ҚАТЕ
            # =================================================

            else:

                usr["fails"] += 1


                if usr["fails"] >= 5:

                    usr["ban_until"] = curr_time + 1800

                    st.error(
                        "⛔ Пароль 5 рет қате жазылды! "
                        "30 мин бан."
                    )

                else:

                    st.error(
                        f"❌ Қате пароль! "
                        f"Қалған мүмкіндік: "
                        f"{5 - usr['fails']}"
                    )


        else:

            st.error(
                "❌ Мұндай қолданушы жоқ!"
            )


# =========================================================
# КІРГЕННЕН КЕЙІН
# =========================================================

else:

    user_info = st.session_state.users[
        st.session_state.logged_user
    ]

    role = user_info["role"]


    # =====================================================
    # ШЫҒУ БАТЫРМАСЫ
    # ОҢ ЖАҚТА
    # =====================================================

    empty_col, logout_col = st.columns(
        [8, 1]
    )


    with logout_col:

        if st.button("Шығу"):

            st.session_state.logged_user = None

            st.rerun()


    # =====================================================
    # ДИРЕКТОР ПАНЕЛІ
    # =====================================================

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


        # =================================================
        # КІРУ ТАРИХЫ
        # =================================================

        with tab1:

            for log in reversed(
                st.session_state.login_logs
            ):

                st.write(
                    f"⏰ **{log['time']}** | "
                    f"👤 Логин: `{log['user']}` "
                    f"({log['role']})"
                )


        # =================================================
        # ЛОГИНДЕР
        # =================================================

        with tab2:

            st.json(
                st.session_state.users
            )


        # =================================================
        # НӘТИЖЕЛЕР
        # =================================================

        with tab3:

            if st.session_state.results:

                for r in st.session_state.results:

                    st.write(
                        f"👤 {r['user']} | "
                        f"📚 Пән: {r['subject']} | "
                        f"🕒 {r['time']} | "
                        f"Балл: {r['score']}"
                    )

            else:

                st.info(
                    "Әзірге тест нәтижелері жоқ."
                )


        # =================================================
        # БАН ШЕШУ
        # =================================================

        with tab4:

            for u_name, u_data in (
                st.session_state.users.items()
            ):

                if u_data["ban_until"] > curr_time:

                    if st.button(
                        f"Unban: {u_name}"
                    ):

                        u_data["ban_until"] = 0

                        u_data["fails"] = 0

                        st.success(
                            f"{u_name} баннан шығарылды!"
                        )

                        st.rerun()


        # =================================================
        # ПАРОЛЬ ЖӘНЕ ДОСТУП
        # =================================================

        with tab5:

            allow_zam = st.checkbox(
                "Зам директорға сұрақ қосуға доступ беру",
                value=st.session_state.can_zam_add_q
            )


            st.session_state.can_zam_add_q = allow_zam


            new_dir_p = st.text_input(
                "Жаңа Директор паролі:",
                type="password",
                key="np_dir"
            )


            if st.button(
                "Директор паролін жаңарту"
            ):

                if new_dir_p.strip():

                    st.session_state.users[
                        "director"
                    ]["pass"] = new_dir_p.strip()

                    st.success(
                        "Директор паролі ауыстырылды!"
                    )


            new_zam_p = st.text_input(
                "Жаңа Зам паролі:",
                type="password",
                key="np_zam"
            )


            if st.button(
                "Зам паролін жаңарту"
            ):

                if new_zam_p.strip():

                    st.session_state.users[
                        "zam"
                    ]["pass"] = new_zam_p.strip()

                    st.success(
                        "Зам паролі ауыстырылды!"
                    )


    # =====================================================
    # ЗАМ / ДИРЕКТОР БАСҚАРУ ПАНЕЛІ
    # =====================================================

    if role == "director" or role == "zam":

        st.subheader(
            "⚙️ Басқару Панелі"
        )


        z_tab1, z_tab2 = st.tabs(
            [
                "📝 Сұрақ Құрастыру",
                "👤 Оқушы Қосу"
            ]
        )


        # =================================================
        # СҰРАҚ ҚҰРАСТЫРУ
        # =================================================

        with z_tab1:

            if (
                role == "zam"
                and not st.session_state.can_zam_add_q
            ):

                st.error(
                    "⛔ Доступ жабық!"
                )

            else:

                selected_sub = st.selectbox(
                    "Пән:",
                    list(
                        st.session_state.questions.keys()
                    )
                )


                q_text = st.text_input(
                    "Сұрақ:"
                )


                col1, col2 = st.columns(2)


                with col1:

                    opt_a = st.text_input(
                        "A жауабы:"
                    )

                    opt_b = st.text_input(
                        "B жауабы:"
                    )


                with col2:

                    opt_c = st.text_input(
                        "C жауабы:"
                    )

                    opt_d = st.text_input(
                        "D жауабы:"
                    )


                correct_opt = st.radio(
                    "Дұрыс нұсқа:",
                    ["A", "B", "C", "D"],
                    horizontal=True
                )


                if st.button(
                    "Сұрақты сақтау"
                ):

                    if (
                        q_text
                        and opt_a
                        and opt_b
                        and opt_c
                        and opt_d
                    ):

                        st.session_state.questions[
                            selected_sub
                        ].append(
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


                        st.success(
                            "✅ Сұрақ қосылды!"
                        )

                    else:

                        st.warning(
                            "⚠️ Барлық жерді толтырыңыз!"
                        )


        # =================================================
        # ОҚУШЫ ҚОСУ
        # =================================================

        with z_tab2:

            new_st_u = st.text_input(
                "Оқушы логині:"
            )


            new_st_p = st.text_input(
                "Оқушы паролі:",
                type="password"
            )


            if st.button(
                "Оқушыны сақтау"
            ):

                if new_st_u and new_st_p:

                    if new_st_u in st.session_state.users:

                        st.error(
                            "❌ Бұл логин бұрыннан бар!"
                        )

                    else:

                        st.session_state.users[
                            new_st_u
                        ] = {

                            "pass": new_st_p,

                            "role": "student",

                            "fails": 0,

                            "ban_until": 0,

                        }


                        st.success(
                            "✅ Оқушы қосылды!"
                        )

                else:

                    st.warning(
                        "⚠️ Логин мен парольді толтырыңыз!"
                    )


    # =====================================================
    # ОҚУШЫ ТЕСТІ
    # =====================================================

    if role == "student":

        st.subheader(
            "📚 Тест"
        )


        subject = st.selectbox(
            "Пән таңдаңыз:",
            list(
                st.session_state.questions.keys()
            )
        )


        q_list = (
            st.session_state.questions[
                subject
            ]
        )


        if q_list:

            user_answers = {}


            for i, q in enumerate(q_list):

                st.write(
                    f"**{i + 1}. {q['q']}**"
                )


                opts = q["options"]


                formatted_opts = [
                    f"{k}) {v}"
                    for k, v in opts.items()
                ]


                ans = st.radio(
                    "Жауап:",
                    formatted_opts,
                    key=f"q_{subject}_{i}"
                )


                user_answers[i] = ans[0]


            # =================================================
            # ТЕСТТІ АЯҚТАУ
            # =================================================

            if st.button(
                "Тестті аяқтау"
            ):

                score = sum(
                    1
                    for i, q in enumerate(q_list)
                    if user_answers.get(i)
                    == q["correct"]
                )


                st.session_state.results.append(
                    {
                        "user":
                            st.session_state.logged_user,

                        "subject":
                            subject,

                        "time":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            ),

                        "score":
                            f"{score}/{len(q_list)}",
                    }
                )


                st.success(
                    f"🎉 Нәтиже: "
                    f"{score} / {len(q_list)}"
                )


        else:

            st.info(
                "Бұл пәнге әзірге сұрақ қосылмаған."
            )
