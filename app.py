import streamlit as st

st.set_page_config(page_title="ҰБТ Тест", page_icon="🎓")


# Логин мен парольді тексеру
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔑 ҰБТ жүйесіне кіру")
        st.text_input("Логин:", key="username")
        st.text_input("Пароль:", type="password", key="password")

        if st.button("Кіру"):
            if (
                st.session_state["username"] == "ubt2026"
                and st.session_state["password"] == "12345"
            ):
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Логин немесе пароль қате!")
        return False
    return True


if check_password():
    st.sidebar.success("Авторизация сәтті өтті!")
    if st.sidebar.button("Шығу"):
        del st.session_state["password_correct"]
        st.rerun()

    st.title("🎓 ҰБТ Онлайн Тестілеу")

    # Сұрақтар базасы
    questions = [
        {
            "question": "Қазақ хандығы қай жылы құрылды?",
            "options": ["1465 ж.", "1456 ж.", "1723 ж.", "1991 ж."],
            "answer": "1465 ж.",
        },
        {
            "question": "sin(90°) неге тең?",
            "options": ["0", "1", "-1", "0.5"],
            "answer": "1",
        },
    ]

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0

    q_idx = st.session_state.current_q

    if q_idx < len(questions):
        q = questions[q_idx]
        st.subheader(f"Сұрақ {q_idx + 1}/{len(questions)}: {q['question']}")

        user_choice = st.radio(
            "Жауапты таңдаңыз:", q["options"], key=f"q_{q_idx}"
        )

        if st.button("Келесі сұрақ ➡️"):
            if user_choice == q["answer"]:
                st.session_state.score += 1
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.balloons()
        st.success(
            f"🎉 Тест аяқталды! Нәтижеңіз: {st.session_state.score} / {len(questions)}"
        )
        if st.button("Қайта тапсыру 🔄"):
            st.session_state.score = 0
            st.session_state.current_q = 0
            st.rerun()
