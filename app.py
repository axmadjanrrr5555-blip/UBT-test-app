import streamlit as st
import json
import os
import time
import random
from datetime import datetime, date, timedelta
import pandas as pd


# =========================================================
# 1. НЕГІЗГІ БАПТАУЛАР
# =========================================================

st.set_page_config(
    page_title="ONLINE TEST PRO",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "app_data.json"

SUBJECTS = [
    "Математика",
    "Қазақстан тарихы",
    "Оқу сауаттылығы",
    "Физика",
    "Химия",
    "Биология",
    "География",
    "Информатика",
    "Қазақ тілі",
    "Қазақ әдебиеті",
    "Ағылшын тілі",
    "Дүниежүзі тарихы",
    "Адам. Қоғам. Құқық"
]

# ҰБТ форматындағы негізгі режим
MAX_TEST_QUESTIONS = 140

# 3 сағат 50 минут
TEST_TIME_SECONDS = 3 * 60 * 60 + 50 * 60

DAILY_GOAL = 50


# =========================================================
# 2. DATA LOAD / SAVE
# =========================================================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    return None


def save_data():
    data = {
        "users": st.session_state.users,
        "questions": st.session_state.questions,
        "results": st.session_state.results,
        "login_logs": st.session_state.login_logs
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# =========================================================
# 3. DATA ИНИЦИАЛИЗАЦИЯ
# =========================================================

saved_data = load_data()


if "users" not in st.session_state:

    if saved_data:

        st.session_state.users = saved_data.get(
            "users",
            {}
        )

        st.session_state.questions = saved_data.get(
            "questions",
            {subject: [] for subject in SUBJECTS}
        )

        st.session_state.results = saved_data.get(
            "results",
            []
        )

        st.session_state.login_logs = saved_data.get(
            "login_logs",
            []
        )

    else:

        st.session_state.users = {

            "director": {
                "name": "Қасым Ахмад (Директор)",
                "pass": "dir123",
                "role": "director",
                "fails": 0,
                "ban_until": 0,
                "attempts": 9999,
                "xp": 0,
                "streak": 0,
                "last_active": "",
                "daily_count": 0,
                "daily_date": ""
            },

            "zam": {
                "name": "Зам Директор",
                "pass": "zam123",
                "role": "zam",
                "fails": 0,
                "ban_until": 0,
                "attempts": 9999,
                "xp": 0,
                "streak": 0,
                "last_active": "",
                "daily_count": 0,
                "daily_date": ""
            }
        }

        st.session_state.questions = {
            subject: []
            for subject in SUBJECTS
        }

        st.session_state.results = []

        st.session_state.login_logs = []


# =========================================================
# 4. SESSION STATE
# =========================================================

defaults = {

    "logged_user": None,

    "last_cert": None,

    "review_result": None,

    "selected_exam_subject": None,

    "test_questions": [],

    "test_answers": {},

    "test_start_time": None,

    "test_deadline": None,

    "test_finished": False,

    "test_mode": "ҰБТ PRO",

    "theme": "dark",

    "page": "home",

    "error_questions": [],

    "daily_goal": DAILY_GOAL

}


for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


curr_time = time.time()


# =========================================================
# 5. USER DATA MIGRATION
# =========================================================

def prepare_user(user):

    if "xp" not in user:
        user["xp"] = 0

    if "streak" not in user:
        user["streak"] = 0

    if "last_active" not in user:
        user["last_active"] = ""

    if "daily_count" not in user:
        user["daily_count"] = 0

    if "daily_date" not in user:
        user["daily_date"] = ""

    if "attempts" not in user:
        user["attempts"] = 5

    if "fails" not in user:
        user["fails"] = 0

    if "ban_until" not in user:
        user["ban_until"] = 0

    return user


for username in st.session_state.users:

    st.session_state.users[username] = prepare_user(
        st.session_state.users[username]
    )


# =========================================================
# 6. QUESTION MIGRATION
# =========================================================

for subject in SUBJECTS:

    if subject not in st.session_state.questions:
        st.session_state.questions[subject] = []


def prepare_question(q):

    if "difficulty" not in q:
        q["difficulty"] = "Орташа"

    if "topic" not in q:
        q["topic"] = "Жалпы"

    if "image" not in q:
        q["image"] = ""

    if "type" not in q:
        q["type"] = "single"

    if "options" not in q:
        q["options"] = {}

    if "correct" not in q:
        q["correct"] = []

    return q


for subject in st.session_state.questions:

    for i in range(
        len(st.session_state.questions[subject])
    ):

        st.session_state.questions[subject][i] = prepare_question(
            st.session_state.questions[subject][i]
        )


# =========================================================
# 7. CSS
# =========================================================

dark_css = """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            #18201d 0%,
            #0b0e14 45%,
            #080a0f 100%
        ) !important;

    font-family:
        'Segoe UI',
        'Trebuchet MS',
        sans-serif;
}

.block-container {
    max-width: 92% !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}

.main-title {
    font-size: 58px;
    font-weight: 900;
    letter-spacing: 5px;
    color: #00ff66 !important;
    text-shadow:
        0 0 10px rgba(0,255,102,.3),
        0 0 30px rgba(0,255,102,.25);
}

.sub-title {
    font-size: 30px;
    font-weight: 800;
    color: #8bffb1 !important;
    letter-spacing: 8px;
}

.hero {
    background:
        linear-gradient(
            135deg,
            rgba(0,255,102,.12),
            rgba(20,25,35,.9)
        );

    border: 1px solid rgba(0,255,102,.25);

    border-radius: 22px;

    padding: 30px;

    margin: 15px 0 25px 0;

    box-shadow:
        0 0 30px rgba(0,255,102,.08);
}

.card {
    background: rgba(19,23,34,.92);

    border: 1px solid #2a2e39;

    border-radius: 18px;

    padding: 22px;

    margin: 10px 0;

    box-shadow:
        0 5px 25px rgba(0,0,0,.25);
}

.stat-card {
    background:
        linear-gradient(
            135deg,
            #151b1d,
            #10151c
        );

    border:
        1px solid rgba(0,255,102,.25);

    border-radius: 16px;

    padding: 20px;

    text-align: center;
}

.stat-number {
    font-size: 35px;
    font-weight: 900;
    color: #00ff66 !important;
}

.stat-label {
    color: #9ba4b0 !important;
    font-size: 15px;
}

.question-box {
    background: #131722;

    border:
        1px solid #2a2e39;

    border-radius: 16px;

    padding: 25px;

    margin: 12px 0;

    box-shadow:
        0 0 20px rgba(0,255,102,.05);
}

.question-number {
    color: #00ff66 !important;
    font-size: 16px;
    font-weight: 800;
}

.question-text {
    color: #ffffff !important;
    font-size: 22px;
    font-weight: 800;
}

.test-header {
    background:
        linear-gradient(
            90deg,
            #111720,
            #142019
        );

    border:
        1px solid #2a2e39;

    border-radius: 15px;

    padding: 15px 20px;

    position: sticky;

    top: 0;

    z-index: 100;
}

.timer {
    color: #00ff66 !important;
    font-size: 28px;
    font-weight: 900;
}

.timer-danger {
    color: #ff4b4b !important;
}

.badge {
    display: inline-block;

    padding: 6px 12px;

    border-radius: 999px;

    background: #1e222d;

    border: 1px solid #00ff66;

    color: #00ff66 !important;

    font-weight: bold;
}

.level {
    font-size: 22px;
    font-weight: 900;
    color: #ffd700 !important;
}

.certificate-box {
    border:
        8px solid #00ff66;

    padding: 45px;

    background:
        linear-gradient(
            135deg,
            #10151c,
            #18211c
        );

    border-radius: 20px;

    text-align: center;

    box-shadow:
        0 0 40px rgba(0,255,102,.25);

    margin: 25px 0;
}

.cert-title {
    font-size: 42px !important;
    font-weight: 900 !important;
    color: #00ff66 !important;
}

.cert-name {
    font-size: 38px !important;
    font-weight: 900 !important;
    color: #ffffff !important;

    border-bottom:
        3px solid #00ff66;

    display: inline-block;

    padding-bottom: 8px;
}

.cert-score {
    font-size: 45px !important;
    font-weight: 900 !important;
    color: #00ff66 !important;
}

.stButton>button {

    background:
        linear-gradient(
            135deg,
            #1b202a,
            #252b37
        ) !important;

    color: #00ff66 !important;

    border:
        1.5px solid #00ff66 !important;

    border-radius: 10px;

    font-weight: 800 !important;

    transition:
        all .2s ease;
}

.stButton>button:hover {

    background:
        #00ff66 !important;

    color:
        #08100c !important;

    box-shadow:
        0 0 20px rgba(0,255,102,.6);
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div {

    background-color:
        #151a24 !important;

    color:
        #00ff66 !important;
}

</style>
"""


light_css = """
<style>

.stApp {
    background: #f4f7f6 !important;
}

.block-container {
    max-width: 92% !important;
}

.main-title {
    color: #07883e !important;
    font-weight: 900;
}

.sub-title {
    color: #126b3d !important;
}

.card,
.question-box,
.stat-card {
    background: white !important;

    border:
        1px solid #d5ddd8;

    border-radius: 18px;

    padding: 22px;

    margin: 10px 0;
}

.question-text {
    color: #111 !important;
}

</style>
"""


if st.session_state.theme == "dark":
    st.markdown(
        dark_css,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        light_css,
        unsafe_allow_html=True
    )


# =========================================================
# 8. HELPER FUNCTIONS
# =========================================================

def today_string():

    return date.today().isoformat()


def get_level(xp):

    return max(
        1,
        xp // 500 + 1
    )


def get_level_progress(xp):

    level = get_level(xp)

    previous = (level - 1) * 500

    current = xp - previous

    return current, 500


def update_activity(username):

    user = st.session_state.users[username]

    today = today_string()

    if user.get("daily_date") != today:

        user["daily_date"] = today
        user["daily_count"] = 0

        yesterday = (
            date.today() -
            timedelta(days=1)
        ).isoformat()

        if user.get("last_active") == yesterday:
            user["streak"] = user.get(
                "streak",
                0
            ) + 1

        else:
            user["streak"] = 1

    user["last_active"] = today


def add_xp(username, amount):

    user = st.session_state.users[username]

    user["xp"] = user.get(
        "xp",
        0
    ) + amount

    update_activity(username)

    user["daily_count"] = user.get(
        "daily_count",
        0
    ) + amount // 10


def get_user_results(username):

    return [
        r for r in st.session_state.results
        if r.get("username") == username
    ]


def get_wrong_questions(username):

    wrong = []

    for result in get_user_results(username):

        for item in result.get(
            "review",
            []
        ):

            if not item.get(
                "is_correct",
                False
            ):

                wrong.append({
                    "subject": result.get(
                        "subject",
                        ""
                    ),
                    **item
                })

    return wrong


def format_time(seconds):

    seconds = max(
        0,
        int(seconds)
    )

    hours = seconds // 3600

    minutes = (
        seconds % 3600
    ) // 60

    secs = seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d}"
    )


def analyze_result(score, total):

    percent = (
        score / total * 100
        if total
        else 0
    )

    if percent >= 90:

        return (
            "🔥 Өте жоғары нәтиже! "
            "Келесі мақсат — нәтижені тұрақты ұстау."
        )

    elif percent >= 75:

        return (
            "🚀 Нәтижең жақсы. "
            "Қателерді қайталап, 90%+ деңгейге ұмтыл."
        )

    elif percent >= 50:

        return (
            "📚 Негізгі тақырыптар қалыптасып келеді. "
            "Қате кеткен сұрақтарды қайта орында."
        )

    else:

        return (
            "🎯 База тақырыптарды қайта қарап, "
            "жеңіл сұрақтардан бастап жаттығу ұсынылады."
        )


def create_test(subject):

    all_questions = (
        st.session_state.questions.get(
            subject,
            []
        )
    )

    if len(all_questions) <= MAX_TEST_QUESTIONS:

        selected = all_questions.copy()

    else:

        selected = random.sample(
            all_questions,
            MAX_TEST_QUESTIONS
        )

    random.shuffle(selected)

    return selected


# =========================================================
# 9. HEADER
# =========================================================

st.markdown(
    '<div class="main-title">ONLINE TEST</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">PRO ACADEMY</div>',
    unsafe_allow_html=True
)

st.write("---")


# =========================================================
# 10. LOGIN
# =========================================================

if not st.session_state.logged_user:

    st.markdown(
        """
        <div class="hero">
            <h1>🎓 ONLINE TEST PRO</h1>
            <p>
                ҰБТ форматына дайындалуға арналған
                заманауи тест платформасы
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔑 Жүйеге кіру")

    col1, col2 = st.columns(2)

    with col1:

        login = st.text_input(
            "Логин:"
        )

    with col2:

        password = st.text_input(
            "Пароль:",
            type="password"
        )

    if st.button(
        "🚀 Кіру",
        use_container_width=True
    ):

        if login in st.session_state.users:

            usr = st.session_state.users[login]

            if usr.get(
                "ban_until",
                0
            ) > curr_time:

                left = int(
                    (
                        usr["ban_until"] -
                        curr_time
                    ) // 60
                )

                st.error(
                    f"⛔ Аккаунт блоктаулы. "
                    f"{left} минут қалды."
                )

            elif usr.get(
                "pass"
            ) == password:

                usr["fails"] = 0

                st.session_state.logged_user = login

                st.session_state.last_cert = None

                st.session_state.review_result = None

                st.session_state.selected_exam_subject = None

                st.session_state.page = "home"

                st.session_state.login_logs.append({
                    "login": login,
                    "time": datetime.now().isoformat()
                })

                save_data()

                st.rerun()

            else:

                usr["fails"] = (
                    usr.get("fails", 0) + 1
                )

                if usr["fails"] >= 10:

                    usr["ban_until"] = (
                        curr_time + 1800
                    )

                    st.error(
                        "⛔ 10 рет қате. "
                        "Аккаунт 30 минутқа блокталды."
                    )

                else:

                    st.error(
                        f"❌ Пароль қате. "
                        f"Қалған мүмкіндік: "
                        f"{10 - usr['fails']}"
                    )

                save_data()

        else:

            st.error(
                "❌ Мұндай қолданушы жоқ."
            )

    st.info(
        "Директор: director / dir123\n\n"
        "Зам директор: zam / zam123"
    )

    st.stop()


# =========================================================
# 11. USER INFO
# =========================================================

username = st.session_state.logged_user

user_info = st.session_state.users[username]

role = user_info.get(
    "role",
    "student"
)

full_name = user_info.get(
    "name",
    username
)

prepare_user(user_info)


# =========================================================
# 12. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        f"## 👋 {full_name}"
    )

    st.markdown(
        f"**Логин:** `{username}`"
    )

    st.markdown(
        "---"
    )

    if role == "student":

        xp = user_info.get(
            "xp",
            0
        )

        level = get_level(xp)

        current_xp, needed_xp = get_level_progress(
            xp
        )

        st.markdown(
            f"### ⭐ Level {level}"
        )

        st.progress(
            min(
                current_xp / needed_xp,
                1.0
            )
        )

        st.caption(
            f"{current_xp} / {needed_xp} XP"
        )

        st.markdown(
            f"🔥 **Streak:** "
            f"{user_info.get('streak', 0)} күн"
        )

        st.markdown(
            f"🎯 **Күндік мақсат:** "
            f"{min(user_info.get('daily_count', 0), DAILY_GOAL)}"
            f"/{DAILY_GOAL}"
        )

    st.markdown("---")

    page = st.radio(
        "Мәзір:",
        [
            "🏠 Басты бет",
            "📝 Тест тапсыру",
            "🧠 Қателерім",
            "📊 Статистика",
            "🏆 Рейтинг"
        ] if role == "student"
        else [
            "🏠 Басқару панелі"
        ]
    )

    st.session_state.page = page

    st.markdown("---")

    if st.session_state.theme == "dark":

        if st.button(
            "☀️ Light Mode",
            use_container_width=True
        ):

            st.session_state.theme = "light"

            st.rerun()

    else:

        if st.button(
            "🌙 Dark Mode",
            use_container_width=True
        ):

            st.session_state.theme = "dark"

            st.rerun()

    st.markdown("---")

    if st.button(
        "🚪 Шығу",
        use_container_width=True
    ):

        st.session_state.logged_user = None

        st.session_state.last_cert = None

        st.session_state.review_result = None

        st.session_state.selected_exam_subject = None

        st.session_state.test_questions = []

        st.session_state.test_answers = {}

        st.rerun()


# =========================================================
# 13. DIRECTOR PANEL
# =========================================================

if role == "director":

    st.title("👨‍💼 Директор панелі")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Сұрақ құрастыру",
        "🗑️ Сұрақтарды басқару",
        "👥 Пайдаланушылар",
        "📊 Нәтижелер",
        "⚙️ Баптаулар"
    ])


    # -----------------------------------------------------
    # TAB 1
    # -----------------------------------------------------

    with tab1:

        st.subheader(
            "📝 Жаңа сұрақ қосу"
        )

        selected_sub = st.selectbox(
            "Пән:",
            SUBJECTS
        )

        q_type = st.selectbox(
            "Сұрақ түрі:",
            [
                "Бір жауапты сұрақ",
                "Көп жауапты сұрақ"
            ]
        )

        difficulty = st.selectbox(
            "Қиындық:",
            [
                "Жеңіл",
                "Орташа",
                "Қиын"
            ]
        )

        topic = st.text_input(
            "📚 Тақырып:"
        )

        q_text = st.text_area(
            "❓ Сұрақ мәтіні:"
        )

        img_url = st.text_input(
            "🖼️ Сурет URL:"
        )

        st.markdown("### Жауап нұсқалары")

        c1, c2 = st.columns(2)

        with c1:

            opt_a = st.text_input("A:")

            opt_b = st.text_input("B:")

            opt_c = st.text_input("C:")

        with c2:

            opt_d = st.text_input("D:")

            opt_e = st.text_input(
                "E:"
            )

            opt_f = st.text_input(
                "F:"
            )

        if q_type == "Бір жауапты сұрақ":

            correct_ans = st.radio(
                "Дұрыс жауап:",
                [
                    "A",
                    "B",
                    "C",
                    "D",
                    "E",
                    "F"
                ],
                horizontal=True
            )

            correct_selected = [
                correct_ans
            ]

        else:

            st.write(
                "Дұрыс жауаптарды таңда:"
            )

            ca = st.checkbox(
                "A",
                key="correct_a"
            )

            cb = st.checkbox(
                "B",
                key="correct_b"
            )

            cc = st.checkbox(
                "C",
                key="correct_c"
            )

            cd = st.checkbox(
                "D",
                key="correct_d"
            )

            ce = st.checkbox(
                "E",
                key="correct_e"
            )

            cf = st.checkbox(
                "F",
                key="correct_f"
            )

            correct_selected = [
                k
                for k, v in zip(
                    [
                        "A",
                        "B",
                        "C",
                        "D",
                        "E",
                        "F"
                    ],
                    [
                        ca,
                        cb,
                        cc,
                        cd,
                        ce,
                        cf
                    ]
                )
                if v
            ]

        if st.button(
            "💾 Сұрақты сақтау",
            use_container_width=True
        ):

            if not q_text:

                st.error(
                    "Сұрақ мәтінін енгіз!"
                )

            elif not (
                opt_a and
                opt_b and
                opt_c and
                opt_d
            ):

                st.error(
                    "A-D жауаптарын толық толтыр!"
                )

            elif not correct_selected:

                st.error(
                    "Дұрыс жауапты таңда!"
                )

            else:

                new_question = {

                    "q": q_text,

                    "type":
                        "single"
                        if q_type ==
                        "Бір жауапты сұрақ"
                        else
                        "multi",

                    "options": {

                        "A": opt_a,
                        "B": opt_b,
                        "C": opt_c,
                        "D": opt_d,
                        "E": opt_e,
                        "F": opt_f
                    },

                    "correct":
                        correct_selected,

                    "image":
                        img_url.strip(),

                    "difficulty":
                        difficulty,

                    "topic":
                        topic.strip()
                        or "Жалпы"
                }

                st.session_state.questions[
                    selected_sub
                ].append(
                    new_question
                )

                save_data()

                st.success(
                    "✅ Сұрақ сәтті қосылды!"
                )


    # -----------------------------------------------------
    # TAB 2
    # -----------------------------------------------------

    with tab2:

        st.subheader(
            "🗑️ Сұрақтарды басқару"
        )

        del_sub = st.selectbox(
            "Пән:",
            SUBJECTS,
            key="delete_subject"
        )

        q_list = (
            st.session_state.questions[
                del_sub
            ]
        )

        st.write(
            f"Барлығы: **{len(q_list)} сұрақ**"
        )

        for idx, q in enumerate(q_list):

            with st.expander(
                f"{idx + 1}. "
                f"{q.get('q', '')}"
            ):

                st.write(
                    f"📚 Тақырып: "
                    f"{q.get('topic', 'Жалпы')}"
                )

                st.write(
                    f"🎯 Қиындық: "
                    f"{q.get('difficulty', 'Орташа')}"
                )

                st.write(
                    f"✅ Дұрыс жауап: "
                    f"{', '.join(q.get('correct', []))}"
                )

                if st.button(
                    "🗑️ Өшіру",
                    key=f"delete_{del_sub}_{idx}"
                ):

                    q_list.pop(idx)

                    save_data()

                    st.success(
                        "Сұрақ өшірілді!"
                    )

                    st.rerun()


    # -----------------------------------------------------
    # TAB 3
    # -----------------------------------------------------

    with tab3:

        st.subheader(
            "👥 Пайдаланушылар"
        )

        user_list = []

        for login_name, user in (
            st.session_state.users.items()
        ):

            user_list.append({

                "Логин":
                    login_name,

                "Аты":
                    user.get(
                        "name",
                        ""
                    ),

                "Рөл":
                    user.get(
                        "role",
                        ""
                    ),

                "XP":
                    user.get(
                        "xp",
                        0
                    ),

                "Level":
                    get_level(
                        user.get(
                            "xp",
                            0
                        )
                    ),

                "Streak":
                    user.get(
                        "streak",
                        0
                    ),

                "Attempts":
                    user.get(
                        "attempts",
                        0
                    )
            })

        st.dataframe(
            pd.DataFrame(
                user_list
            ),
            use_container_width=True
        )

        st.markdown(
            "### ➕ Жаңа пайдаланушы"
        )

        add_role = st.selectbox(
            "Рөл:",
            [
                "student",
                "zam"
            ],
            key="add_role"
        )

        name_in = st.text_input(
            "Аты-жөні:",
            key="new_name"
        )

        log_in = st.text_input(
            "Логин:",
            key="new_login"
        )

        pas_in = st.text_input(
            "Пароль:",
            type="password",
            key="new_pass"
        )

        if st.button(
            "➕ Қосу",
            use_container_width=True
        ):

            if (
                name_in and
                log_in and
                pas_in
            ):

                if log_in in st.session_state.users:

                    st.error(
                        "Бұл логин бар!"
                    )

                else:

                    st.session_state.users[
                        log_in
                    ] = {

                        "name":
                            name_in,

                        "pass":
                            pas_in,

                        "role":
                            add_role,

                        "fails":
                            0,

                        "ban_until":
                            0,

                        "attempts":
                            5,

                        "xp":
                            0,

                        "streak":
                            0,

                        "last_active":
                            "",

                        "daily_count":
                            0,

                        "daily_date":
                            ""
                    }

                    save_data()

                    st.success(
                        "Пайдаланушы қосылды!"
                    )

                    st.rerun()

            else:

                st.error(
                    "Барлық өрісті толтыр!"
                )


    # -----------------------------------------------------
    # TAB 4
    # -----------------------------------------------------

    with tab4:

        st.subheader(
            "📊 Барлық тест нәтижелері"
        )

        if st.session_state.results:

            rows = []

            for r in (
                st.session_state.results
            ):

                rows.append({

                    "Оқушы":
                        r.get(
                            "name",
                            ""
                        ),

                    "Пән":
                        r.get(
                            "subject",
                            ""
                        ),

                    "Ұпай":
                        f"{r.get('score', 0)} / "
                        f"{r.get('total', 0)}",

                    "Пайыз":
                        f"{r.get('percent', 0):.1f}%",

                    "Күні":
                        r.get(
                            "date",
                            ""
                        )
                })

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True
            )

        else:

            st.info(
                "Әзірге нәтиже жоқ."
            )


    # -----------------------------------------------------
    # TAB 5
    # -----------------------------------------------------

    with tab5:

        st.subheader(
            "⚙️ Директор баптаулары"
        )

        old_p = st.text_input(
            "Ескі пароль:",
            type="password"
        )

        new_p = st.text_input(
            "Жаңа пароль:",
            type="password"
        )

        if st.button(
            "🔐 Парольді өзгерту"
        ):

            if old_p == user_info.get(
                "pass"
            ):

                if new_p:

                    user_info["pass"] = new_p

                    save_data()

                    st.success(
                        "Пароль өзгертілді!"
                    )

                else:

                    st.error(
                        "Жаңа пароль енгіз!"
                    )

            else:

                st.error(
                    "Ескі пароль қате!"
                )


# =========================================================
# 14. ZAM DIRECTOR
# =========================================================

elif role == "zam":

    st.title(
        "🛠️ Зам директор панелі"
    )

    st.info(
        "Бұл бөлім арқылы тест сұрақтарын қосуға болады."
    )

    selected_sub = st.selectbox(
        "Пән:",
        SUBJECTS
    )

    difficulty = st.selectbox(
        "Қиындық:",
        [
            "Жеңіл",
            "Орташа",
            "Қиын"
        ],
        key="zam_difficulty"
    )

    topic = st.text_input(
        "Тақырып:",
        key="zam_topic"
    )

    q_text = st.text_area(
        "Сұрақ:",
        key="zam_question"
    )

    c1, c2 = st.columns(2)

    with c1:

        oa = st.text_input(
            "A:",
            key="zam_a"
        )

        ob = st.text_input(
            "B:",
            key="zam_b"
        )

        oc = st.text_input(
            "C:",
            key="zam_c"
        )

    with c2:

        od = st.text_input(
            "D:",
            key="zam_d"
        )

        oe = st.text_input(
            "E:",
            key="zam_e"
        )

        of = st.text_input(
            "F:",
            key="zam_f"
        )

    cor = st.radio(
        "Дұрыс жауап:",
        [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F"
        ],
        horizontal=True,
        key="zam_correct"
    )

    if st.button(
        "💾 Сұрақты сақтау",
        use_container_width=True
    ):

        if (
            q_text and
            oa and
            ob and
            oc and
            od
        ):

            st.session_state.questions[
                selected_sub
            ].append({

                "q":
                    q_text,

                "type":
                    "single",

                "options": {

                    "A": oa,
                    "B": ob,
                    "C": oc,
                    "D": od,
                    "E": oe,
                    "F": of
                },

                "correct":
                    [cor],

                "image":
                    "",

                "difficulty":
                    difficulty,

                "topic":
                    topic or "Жалпы"
            })

            save_data()

            st.success(
                "✅ Сұрақ сақталды!"
            )

        else:

            st.error(
                "A-D және сұрақты толық толтыр!"
            )


# =========================================================
# 15. STUDENT
# =========================================================

elif role == "student":

    # =====================================================
    # 15.1 HOME
    # =====================================================

    if page == "🏠 Басты бет":

        st.markdown(
            f"""
            <div class="hero">
                <h1>👋 Сәлем, {full_name}!</h1>
                <p>
                    Бүгінгі мақсатыңды орындап,
                    өз нәтижеңді көтер.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        xp = user_info.get(
            "xp",
            0
        )

        level = get_level(xp)

        daily = min(
            user_info.get(
                "daily_count",
                0
            ),
            DAILY_GOAL
        )

        cols = st.columns(4)

        with cols[0]:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">
                        ⭐ {xp}
                    </div>
                    <div class="stat-label">
                        XP
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[1]:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">
                        🟢 {level}
                    </div>
                    <div class="stat-label">
                        LEVEL
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[2]:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">
                        🔥 {user_info.get('streak', 0)}
                    </div>
                    <div class="stat-label">
                        STREAK
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with cols[3]:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-number">
                        🎯 {daily}/{DAILY_GOAL}
                    </div>
                    <div class="stat-label">
                        БҮГІН
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "### 🎯 Бүгінгі мақсат"
        )

        st.progress(
            daily / DAILY_GOAL
        )

        st.markdown(
            "### 🚀 Тестті бастау"
        )

        cols = st.columns(3)

        for i, subject in enumerate(
            SUBJECTS[:6]
        ):

            with cols[i % 3]:

                question_count = len(
                    st.session_state.questions[
                        subject
                    ]
                )

                st.markdown(
                    f"""
                    <div class="card">
                        <h3>📚 {subject}</h3>
                        <p>
                            {question_count}
                            сұрақ дайын
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"▶️ {subject}",
                    key=f"home_test_{i}",
                    use_container_width=True
                ):

                    if question_count > 0:

                        st.session_state.selected_exam_subject = subject

                        st.session_state.test_questions = create_test(
                            subject
                        )

                        st.session_state.test_answers = {}

                        st.session_state.test_start_time = time.time()

                        st.session_state.test_deadline = (
                            time.time() +
                            TEST_TIME_SECONDS
                        )

                        st.session_state.test_finished = False

                        st.session_state.page = "📝 Тест тапсыру"

                        st.rerun()

                    else:

                        st.warning(
                            "Бұл пәнде сұрақ жоқ."
                        )


    # =====================================================
    # 15.2 TEST
    # =====================================================

    elif page == "📝 Тест тапсыру":

        subject = (
            st.session_state.selected_exam_subject
        )

        questions = (
            st.session_state.test_questions
        )

        if not subject or not questions:

            st.markdown(
                """
                <div class="hero">
                    <h1>🎯 ҰБТ PRO</h1>
                    <p>
                        Пәнді таңда да тестті баста.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            subject_select = st.selectbox(
                "📚 Пән:",
                SUBJECTS
            )

            count = len(
                st.session_state.questions[
                    subject_select
                ]
            )

            st.info(
                f"Бұл пәнде {count} сұрақ бар."
            )

            if st.button(
                "🚀 140 форматындағы тестті бастау",
                use_container_width=True
            ):

                if count == 0:

                    st.error(
                        "Бұл пәнде сұрақ жоқ!"
                    )

                else:

                    st.session_state.selected_exam_subject = subject_select

                    st.session_state.test_questions = create_test(
                        subject_select
                    )

                    st.session_state.test_answers = {}

                    st.session_state.test_start_time = time.time()

                    st.session_state.test_deadline = (
                        time.time() +
                        TEST_TIME_SECONDS
                    )

                    st.session_state.test_finished = False

                    st.rerun()

        else:

            total = len(
                questions
            )

            remaining = (
                st.session_state.test_deadline -
                time.time()
            )

            if remaining <= 0:

                st.session_state.test_finished = True

            # TEST HEADER

            progress = (
                len(
                    st.session_state.test_answers
                )
                / total
            )

            st.markdown(
                f"""
                <div class="test-header">
                    <div style="display:flex;
                                justify-content:space-between;
                                align-items:center;">

                        <div>
                            <b>
                                📚 {subject}
                            </b>
                            <br>
                            <small>
                                {total} сұрақ
                            </small>
                        </div>

                        <div class="timer">
                            ⏱️ {format_time(remaining)}
                        </div>

                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                progress
            )

            st.caption(
                f"Жауап берілді: "
                f"{len(st.session_state.test_answers)} / {total}"
            )

            # 140 QUESTION NAVIGATION

            st.markdown(
                "### 🔢 Сұрақтар"
            )

            nav_cols = st.columns(
                10
            )

            for i in range(total):

                with nav_cols[i % 10]:

                    answered = (
                        i in
                        st.session_state.test_answers
                    )

                    if answered:

                        st.markdown(
                            f"""
                            <div style="
                            background:#00ff66;
                            color:#08100c;
                            padding:6px;
                            border-radius:8px;
                            text-align:center;
                            font-weight:900;">
                            {i+1}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f"""
                            <div style="
                            background:#242936;
                            color:#ffffff;
                            padding:6px;
                            border-radius:8px;
                            text-align:center;">
                            {i+1}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            st.markdown("---")

            # QUESTIONS

            for i, q in enumerate(
                questions
            ):

                st.markdown(
                    f"""
                    <div class="question-box">

                        <div class="question-number">
                            ❓ {i+1}-СҰРАҚ
                        </div>

                        <div class="question-text">
                            {q.get('q', '')}
                        </div>

                        <br>

                        <span class="badge">
                            {q.get('difficulty', 'Орташа')}
                        </span>

                        <span class="badge">
                            📚 {q.get('topic', 'Жалпы')}
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if q.get(
                    "image",
                    ""
                ):

                    try:

                        st.image(
                            q["image"],
                            width=500
                        )

                    except Exception:

                        st.warning(
                            "Суретті жүктеу мүмкін болмады."
                        )

                options = [
                    f"{k}) {v}"
                    for k, v in q.get(
                        "options",
                        {}
                    ).items()
                    if v and str(v).strip()
                ]

                if q.get(
                    "type"
                ) == "multi":

                    selected = st.multiselect(
                        "Бірнеше жауап таңда:",
                        options,
                        key=f"multi_answer_{i}"
                    )

                    answer_letters = [
                        x[0]
                        for x in selected
                    ]

                else:

                    selected = st.radio(
                        "Жауапты таңда:",
                        options,
                        index=None,
                        key=f"single_answer_{i}"
                    )

                    answer_letters = (
                        [selected[0]]
                        if selected
                        else []
                    )

                st.session_state.test_answers[i] = (
                    answer_letters
                )

            st.markdown("---")

            # FINISH

            if st.session_state.test_finished:

                st.warning(
                    "⏰ Уақыт аяқталды! "
                    "Тест автоматты түрде тексеріледі."
                )

            if st.button(
                "🚀 ТЕСТТІ АЯҚТАУ",
                use_container_width=True
            ) or st.session_state.test_finished:

                score = 0

                review_data = []

                for i, q in enumerate(
                    questions
                ):

                    user_ans = set(
                        st.session_state.test_answers.get(
                            i,
                            []
                        )
                    )

                    correct_ans = set(
                        q.get(
                            "correct",
                            []
                        )
                    )

                    is_correct = (
                        user_ans ==
                        correct_ans
                        and
                        len(user_ans) > 0
                    )

                    if is_correct:

                        score += 1

                    review_data.append({

                        "q_num":
                            i + 1,

                        "question":
                            q.get(
                                "q",
                                ""
                            ),

                        "user_ans":
                            list(user_ans),

                        "correct_ans":
                            list(correct_ans),

                        "is_correct":
                            is_correct,

                        "topic":
                            q.get(
                                "topic",
                                "Жалпы"
                            ),

                        "difficulty":
                            q.get(
                                "difficulty",
                                "Орташа"
                            )
                    })

                percent = (
                    score /
                    total *
                    100
                ) if total else 0

                # XP

                earned_xp = (
                    score * 10
                    + 100
                )

                add_xp(
                    username,
                    earned_xp
                )

                # RESULT

                result = {

                    "username":
                        username,

                    "name":
                        full_name,

                    "subject":
                        subject,

                    "score":
                        score,

                    "total":
                        total,

                    "percent":
                        percent,

                    "date":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        ),

                    "review":
                        review_data
                }

                st.session_state.results.append(
                    result
                )

                # CERTIFICATE

                st.session_state.last_cert = {

                    "user_fullname":
                        full_name,

                    "subject":
                        subject,

                    "score":
                        f"{score} / {total}",

                    "percent":
                        percent,

                    "rank":
                        1
                }

                st.session_state.review_result = (
                    review_data
                )

                st.session_state.test_questions = []

                st.session_state.test_answers = {}

                st.session_state.selected_exam_subject = None

                st.session_state.test_finished = False

                save_data()

                st.session_state.page = "📊 Статистика"

                st.rerun()


    # =====================================================
    # 15.3 ERRORS
    # =====================================================

    elif page == "🧠 Қателерім":

        st.title(
            "🧠 Менің қателерім"
        )

        wrong = get_wrong_questions(
            username
        )

        if not wrong:

            st.success(
                "🔥 Қате сұрақтарың жоқ!"
            )

        else:

            st.write(
                f"Барлығы: **{len(wrong)} қате**"
            )

            for i, item in enumerate(
                wrong
            ):

                with st.expander(
                    f"❌ {i+1}. "
                    f"{item['question']}"
                ):

                    st.write(
                        f"📚 Пән: "
                        f"{item['subject']}"
                    )

                    st.write(
                        f"🎯 Тақырып: "
                        f"{item.get('topic', 'Жалпы')}"
                    )

                    st.write(
                        f"Сенің жауабың: "
                        f"`{', '.join(item.get('user_ans', [])) or 'Бос'}"
                        "`"
                    )

                    st.write(
                        f"Дұрыс жауап: "
                        f"`{', '.join(item.get('correct_ans', []))}`"
                    )


    # =====================================================
    # 15.4 STATISTICS
    # =====================================================

    elif page == "📊 Статистика":

        st.title(
            "📊 Менің статистикам"
        )

        results = get_user_results(
            username
        )

        if not results:

            st.info(
                "Әзірге тест тапсырмадың."
            )

        else:

            total_tests = len(
                results
            )

            avg_percent = sum(
                r.get(
                    "percent",
                    0
                )
                for r in results
            ) / total_tests

            best = max(
                results,
                key=lambda x:
                    x.get(
                        "percent",
                        0
                    )
            )

            cols = st.columns(3)

            with cols[0]:

                st.metric(
                    "📝 Тест саны",
                    total_tests
                )

            with cols[1]:

                st.metric(
                    "📈 Орташа нәтиже",
                    f"{avg_percent:.1f}%"
                )

            with cols[2]:

                st.metric(
                    "🏆 Ең жоғары",
                    f"{best.get('percent', 0):.1f}%"
                )

            st.markdown(
                "### 📚 Пәндер бойынша"
            )

            subject_stats = {}

            for r in results:

                sub = r.get(
                    "subject",
                    ""
                )

                subject_stats.setdefault(
                    sub,
                    []
                )

                subject_stats[sub].append(
                    r.get(
                        "percent",
                        0
                    )
                )

            stat_rows = []

            for sub, values in (
                subject_stats.items()
            ):

                stat_rows.append({

                    "Пән":
                        sub,

                    "Тест саны":
                        len(values),

                    "Орташа":
                        f"{sum(values)/len(values):.1f}%",

                    "Ең жоғары":
                        f"{max(values):.1f}%"
                })

            st.dataframe(
                pd.DataFrame(
                    stat_rows
                ),
                use_container_width=True
            )

            st.markdown(
                "### 🧠 Соңғы нәтижелер"
            )

            for r in reversed(
                results[-10:]
            ):

                percent = r.get(
                    "percent",
                    0
                )

                st.markdown(
                    f"""
                    <div class="card">

                        <b>
                            📚 {r.get('subject', '')}
                        </b>

                        <br>

                        🎯
                        {r.get('score', 0)}
                        /
                        {r.get('total', 0)}

                        —

                        <b>
                            {percent:.1f}%
                        </b>

                        <br>

                        <small>
                            {r.get('date', '')}
                        </small>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # last result analysis

            last = results[-1]

            st.markdown(
                "### 🤖 Автоматты талдау"
            )

            st.info(
                analyze_result(
                    last.get("score", 0),
                    last.get("total", 0)
                )
            )

            # certificate

            if st.session_state.last_cert:

                cert = (
                    st.session_state.last_cert
                )

                st.markdown(
                    f"""
                    <div class="certificate-box">

                        <div class="cert-title">
                            🏆 СЕРТИФИКАТ 🏆
                        </div>

                        <p>
                            ONLINE TEST PRO ACADEMY
                        </p>

                        <p>
                            Бұл сертификат
                        </p>

                        <div class="cert-name">
                            {cert['user_fullname']}
                        </div>

                        <p>
                            {cert['subject']}
                            пәнінен тест тапсырды.
                        </p>

                        <div class="cert-score">
                            {cert['score']}
                        </div>

                        <p>
                            Нәтиже:
                            {cert['percent']:.1f}%
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # =====================================================
    # 15.5 LEADERBOARD
    # =====================================================

    elif page == "🏆 Рейтинг":

        st.title(
            "🏆 ONLINE TEST рейтингі"
        )

        students = []

        for login_name, user in (
            st.session_state.users.items()
        ):

            if user.get(
                "role"
            ) == "student":

                students.append({

                    "name":
                        user.get(
                            "name",
                            login_name
                        ),

                    "xp":
                        user.get(
                            "xp",
                            0
                        ),

                    "level":
                        get_level(
                            user.get(
                                "xp",
                                0
                            )
                        ),

                    "streak":
                        user.get(
                            "streak",
                            0
                        )
                })

        students.sort(
            key=lambda x:
                x["xp"],
            reverse=True
        )

        if not students:

            st.info(
                "Рейтингте әзірге оқушылар жоқ."
            )

        else:

            for i, student in enumerate(
                students
            ):

                if i == 0:

                    medal = "🥇"

                elif i == 1:

                    medal = "🥈"

                elif i == 2:

                    medal = "🥉"

                else:

                    medal = f"{i+1}."

                st.markdown(
                    f"""
                    <div class="card">

                        <h3>
                            {medal}
                            {student['name']}
                        </h3>

                        ⭐
                        {student['xp']} XP

                        &nbsp;&nbsp;

                        🟢
                        Level {student['level']}

                        &nbsp;&nbsp;

                        🔥
                        {student['streak']} күн

                    </div>
                    """,
                    unsafe_allow_html=True
                )
