import streamlit as st
import json
import os

st.set_page_config(page_title="ONLINE TEST PRO", layout="wide")

DATA_FILE = "app_data.json"

SUBJECTS = [
    "Математика", "Физика", "Химия", "Биология",
    "Информатика", "Қазақстан тарихы", "География",
    "Қазақ тілі", "Ағылшын тілі"
]

QUESTION_LIMITS = {s: 40 for s in SUBJECTS}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Деректерді жүктеу, ЕШҚАШАН өшірілмейді ---
if "data" not in st.session_state:
    d = load_data()
    if d is None or "questions" not in d:
        d = {"questions": {s: [] for s in SUBJECTS}, "results": []}
        save_data(d)
    # жаңа пән қосылса, оны толықтырамыз, барын өшірмейміз
    for s in SUBJECTS:
        if s not in d["questions"]:
            d["questions"][s] = []
    st.session_state.data = d

if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "test_questions" not in st.session_state:
    st.session_state.test_questions = []
if "page" not in st.session_state:
    st.session_state.page = "test"

st.title("ONLINE TEST PRO")

menu = st.sidebar.radio("Мәзір:", ["Тест тапсыру", "Сұрақ қосу (Админ)"])
subject = st.selectbox("Пән таңда:", SUBJECTS)

# --- КАЛЬКУЛЯТОР МЕН МЕНДЕЛЕЕВ - әрқашан көрінеді ---
col_calc, col_mend = st.columns(2)
with col_calc:
    with st.expander("🧮 Калькулятор"):
        calc = st.text_input("Есеп жаз:", key="calc_input")
        if calc:
            try:
                # тек сандарға рұқсат
                allowed = "0123456789+-*/(). "
                if all(c in allowed for c in calc):
                    st.write("Нәтиже:", eval(calc))
                else:
                    st.error("Тек сандар мен + - * / жаз")
            except:
                st.error("Қате өрнек")

with col_mend:
    with st.expander("🧪 Менделеев кестесі"):
        st.markdown("""
        | H | | | | | | | He |
        | Li | Be | B | C | N | O | F | Ne |
        | Na | Mg | Al | Si | P | S | Cl | Ar |
        | K | Ca | ... | ... | ... | ... | ... | ... |
        """)
        st.caption("H-1 He-4 Li-7 Be-9 B-11 C-12 N-14 O-16 F-19 Ne-20 Na-23 Mg-24 Al-27 Si-28 P-31 S-32 Cl-35.5 Ar-40 K-39 Ca-40")

# --- СҰРАҚ ҚОСУ ---
if menu == "Сұрақ қосу (Админ)":
    st.subheader(f"Сұрақ қосу: {subject}")
    q_text = st.text_area("Сұрақ мәтіні:")
    opt_a = st.text_input("A жауабы:")
    opt_b = st.text_input("B жауабы:")
    opt_c = st.text_input("C жауабы:")
    opt_d = st.text_input("D жауабы:")
    correct = st.selectbox("Дұрыс жауап:", ["A","B","C","D"])

    if st.button("Сақтау"):
        if q_text and opt_a and opt_b:
            new_q = {
                "text": q_text,
                "options": [opt_a, opt_b, opt_c, opt_d],
                "correct": correct
            }
            st.session_state.data["questions"][subject].append(new_q)
            save_data(st.session_state.data)
            st.success(f"Сақталды! Барлығы: {len(st.session_state.data['questions'][subject])}")
        else:
            st.warning("Сұрақ пен жауаптарды толтыр")

    st.info(f"Бұл пәнде: {len(st.session_state.data['questions'][subject])} сұрақ бар")

# --- ТЕСТ ТАПСЫРУ ---
else:
    if not st.session_state.test_started:
        count = len(st.session_state.data["questions"][subject])
        st.write(f"Қолда сұрақ саны: {count}")

        if st.button("Тестті бастау"):
            qs = st.session_state.data["questions"].get(subject, [])
            if not qs:
                st.warning("Сұрақ жоқ. Алдымен Админ бөлімінде қос.")
            else:
                st.session_state.test_questions = qs[:QUESTION_LIMITS[subject]]
                st.session_state.test_started = True
                st.rerun()
    else:
        st.subheader(f"Тест: {subject}")
        for i, q in enumerate(st.session_state.test_questions):
            st.write(f"**{i+1}. {q.get('text','')}**")
            st.radio("Жауап:", q.get("options", []), key=f"ans_{subject}_{i}", index=None)

        if st.button("Тестті аяқтау"):
            score = 0
            for i, q in enumerate(st.session_state.test_questions):
                user_ans_idx = st.session_state.get(f"ans_{subject}_{i}")
                # radio индекс қайтарады, оны әріпке айналдырамыз
                letters = ["A","B","C","D"]
                if user_ans_idx is not None:
                    # options тізімінен таңдалған мән
                    chosen = user_ans_idx
                    opts = q.get("options", [])
                    if chosen in opts:
                        chosen_letter = letters[opts.index(chosen)]
                        if chosen_letter == q.get("correct"):
                            score += 1
            st.success(f"Нәтиже: {score} / {len(st.session_state.test_questions)}")
            # СҰРАҚТАР ӨШІРІЛМЕЙДІ! Тек тест жабылады
            st.session_state.test_started = False

        if st.button("Тесттен шығу (сұрақтар сақталады)"):
            st.session_state.test_started = False
            st.rerun()
