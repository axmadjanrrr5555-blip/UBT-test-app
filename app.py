from datetime import datetime
import json
import os
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ONLINE TEST SYSTEM", layout="wide", page_icon="📜"
)

# --- ФАЙЛҒА САҚТАУ ЖӘНЕ ОҚУ ---
DATA_FILE = "app_data.json"


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return None


def save_data():
  data = {
      "users": st.session_state.users,
      "questions": st.session_state.questions,
      "results": st.session_state.results,
      "login_logs": st.session_state.login_logs,
  }
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# --- SESSION STATE ИНИЦИАЛИЗАЦИЯСЫ ---
saved_data = load_data()

if "users" not in st.session_state:
  if saved_data:
    st.session_state.users = saved_data.get("users", {})
    st.session_state.questions = saved_data.get("questions", {})
    st.session_state.results = saved_data.get("results", [])
    st.session_state.login_logs = saved_data.get("login_logs", [])
  else:
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
    st.session_state.results = []
    st.session_state.login_logs = []

if "logged_user" not in st.session_state:
  st.session_state.logged_user = None
if "last_cert" not in st.session_state:
  st.session_state.last_cert = None
if "review_result" not in st.session_state:
  st.session_state.review_result = None
if "selected_exam_subject" not in st.session_state:
  st.session_state.selected_exam_subject = None

curr_time = time.time()

# --- ТОЛЫҚ ДИЗАЙН ЖӘНЕ СТИЛЬДЕР ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14 !important;
        background-image: radial-gradient(circle at 50% 20%, #131722 0%, #0b0e14 100%);
        font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
    }
    
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

    /* СҰРАҚТАР БӨЛІМІ (Шетке шығып кетпейтін етіп ортаға тураланған) */
    .question-box {
        width: 100% !important;
        max-width: 800px;
        margin: 0 auto 20px auto;
        background: #131722;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #2a2e39;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.1);
    }
    
    .question-box h4, .question-box p, .question-box label {
        font-size: 20px !important;
        color: #D1D4DC !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span, small, li { 
        color: #D1D4DC !important; 
        font-weight: 600 !important;
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

    /* ӘДЕМІ СЕРТИФИКАТ СТИЛІ */
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
        font-size: 42px !important;
        font-weight: 900 !important;
        color: #00FF66 !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .cert-academy {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #848e9c !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .cert-name {
        font-size: 38px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        border-bottom: 3px solid #00FF66;
        display: inline-block;
        padding-bottom: 5px;
        margin: 15px 0;
    }
    .cert-body {
        font-size: 20px !important;
        color: #D1D4DC !important;
        margin: 10px 0;
    }
    .cert-score {
        font-size: 40px !important;
        font-weight: bold !important;
        color: #00FF66 !important;
        margin: 5px 0;
    }
    .cert-rank {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #FFD700 !important;
        background: #1e222d;
        display: inline-block;
        padding: 8px 20px;
        border-radius: 8px;
        border: 1.5px solid #FFD700;
        margin: 15px 0;
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
          usr["fails"] = 0
          st.session_state.logged_user = login
          st.session_state.last_cert = None
          st.session_state.review_result = None
          st.session_state.selected_exam_subject = None
          save_data()
          st.rerun()
        else:
          usr["fails"] += 1
          if usr["fails"] >= 10:
            usr["ban_until"] = curr_time + 1800
            st.error("⛔ 10 рет қате! Аккаунт 30 минутқа БАНДАЛДЫ.")
          else:
            st.error(f"❌ Қате пароль! Қалған мүмкіндік: {10 - usr['fails']}")
          save_data()
      else:
        st.error("❌ Мұндай қолданушы жоқ!")

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

  if role == "student":
    st.sidebar.markdown(f"🔑 **Қалған доступ:** `{user_info.get('attempts', 0)}`")
    if st.session_state.selected_exam_subject:
      st.sidebar.markdown(
          f"📚 **Пән:** `{st.session_state.selected_exam_subject}`"
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
            "🗑️ Сұрақтарды Басқару",
            "👥 Пайдаланушылар",
            "⚙️ Баптаулар",
        ]
    )

    with tab1:
      selected_sub = st.selectbox(
          "Пәнді таңдаңыз:", list(st.session_state.questions.keys())
      )
      q_type = st.selectbox(
          "Түрі:", ["Бір жауапты сұрақ", "Көп жауапты сұрақ"]
      )
      q_text = st.text_input("Сұрақ мәтіні:")
      img_url = st.text_input("🖼️ Сурет сілтемесі (URL):")

      c1, c2 = st.columns(2)
      with c1:
        opt_a = st.text_input("A:")
        opt_b = st.text_input("B:")
        opt_c = st.text_input("C:")
      with c2:
        opt_d = st.text_input("D:")
        opt_e = st.text_input("E (міндетті емес):")
        opt_f = st.text_input("F (міндетті емес):")

      if q_type == "Бір жауапты сұрақ":
        correct_ans = st.radio(
            "Дұрыс жауап:", ["A", "B", "C", "D", "E", "F"], key="dir_single"
        )
        correct_selected = [correct_ans]
      else:
        st.write("Дұрыс жауаптар:")
        ca, cb, cc = st.checkbox("A"), st.checkbox("B"), st.checkbox("C")
        cd, ce, cf = st.checkbox("D"), st.checkbox("E"), st.checkbox("F")
        correct_selected = [
            k
            for k, v in zip(
                ["A", "B", "C", "D", "E", "F"], [ca, cb, cc, cd, ce, cf]
            )
            if v
        ]

      if st.button("Сұрақты Сақтау"):
        if not q_text or not (opt_a and opt_b and opt_c and opt_d):
          st.error("⚠️ Өрістерді толық толтырыңыз!")
        elif not correct_selected:
          st.error("⚠️ Дұрыс жауапты белгілеңіз!")
        else:
          st.session_state.questions[selected_sub].append({
              "q": q_text,
              "type": "single" if q_type == "Бір жауапты сұрақ" else "multi",
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
          })
          save_data()
          st.success("✅ Сұрақ сақталды!")

    with tab2:
      del_sub = st.selectbox(
          "Пәнді таңдаңыз:",
          list(st.session_state.questions.keys()),
          key="del_sub",
      )
      q_list = st.session_state.questions[del_sub]
      for idx, q in enumerate(q_list):
        st.markdown(f"**{idx+1}. {q['q']}**")
        if st.button("🗑️ Өшіру", key=f"del_{del_sub}_{idx}"):
          q_list.pop(idx)
          save_data()
          st.success("Өшірілді!")
          st.rerun()

    with tab3:
      st.subheader("👥 Пайдаланушылар тізімі")
      user_list = [
          {
              "Логин": k,
              "Аты": v.get("name"),
              "Пароль": v.get("pass"),
              "Рөл": v.get("role"),
          }
          for k, v in st.session_state.users.items()
      ]
      st.dataframe(pd.DataFrame(user_list), use_container_width=True)

      st.subheader("➕ Оқушы немесе Зам қосу")
      add_role = st.selectbox("Рөлі:", ["zam", "student"])
      name_in = st.text_input("Аты-жөні:")
      log_in = st.text_input("Логин (жаңа):")
      pas_in = st.text_input("Пароль (жаңа):")

      if st.button("Қосу"):
        if log_in and pas_in and name_in:
          st.session_state.users[log_in] = {
              "name": name_in,
              "pass": pas_in,
              "role": add_role,
              "fails": 0,
              "ban_until": 0,
              "attempts": 5,
          }
          save_data()
          st.success("Сәтті қосылды!")
          st.rerun()

    with tab4:
      st.subheader("⚙️ Парольді өзгерту")
      old_p = st.text_input("Ескі пароль:", type="password")
      new_p1 = st.text_input("Жаңа пароль:", type="password")
      if st.button("Өзгерту"):
        usr_obj = st.session_state.users[st.session_state.logged_user]
        if old_p == usr_obj["pass"]:
          usr_obj["pass"] = new_p1
          save_data()
          st.success("Пароль өзгерді!")
        else:
          st.error("Ескі пароль қате!")

  # --- ЗАМ ДИРЕКТОР ПАНЕЛІ ---
  if role == "zam":
    st.subheader("🛠️ Зам панелі (Сұрақ қосу)")
    selected_sub = st.selectbox(
        "Пән:", list(st.session_state.questions.keys()), key="z_sub"
    )
    q_text = st.text_input("Сұрақ:", key="z_q")
    c1, c2 = st.columns(2)
    with c1:
      oa, ob, oc = (
          st.text_input("A:", key="za"),
          st.text_input("B:", key="zb"),
          st.text_input("C:", key="zc"),
      )
    with c2:
      od, oe, of = (
          st.text_input("D:", key="zd"),
          st.text_input("E:", key="ze"),
          st.text_input("F:", key="zf"),
      )
    cor = st.radio("Дұрыс жауап:", ["A", "B", "C", "D", "E", "F"], key="z_cor")

    if st.button("Сақтау (Зам)"):
      if q_text and oa and ob and oc and od:
        st.session_state.questions[selected_sub].append({
            "q": q_text,
            "type": "single",
            "options": {"A": oa, "B": ob, "C": oc, "D": od, "E": oe, "F": of},
            "correct": [cor],
            "image": "",
        })
        save_data()
        st.success("Сақталды!")

  # --- ОҚУШЫ ТЕСТІ ЖӘНЕ ҚАТЕЛЕРДІ ТАЛДАУ ---
  if role == "student":
    if st.session_state.last_cert:
      cert = st.session_state.last_cert

      # Әдемі сертификат толық дизайнымен
      st.markdown(
          f"""
            <div class="certificate-box">
                <div class="cert-title">🏆 СЕРТИФИКАТ 🏆</div>
                <div class="cert-academy">ONLINE TEST ACADEMY</div>
                <p class="cert-body">Осы сертификат табысты тест тапсырған оқушыға беріледі:</p>
                <div class="cert-name">{cert['user_fullname']}</div>
                <br>
                <p class="cert-body">Пән: <b>{cert['subject']}</b></p>
                <div class="cert-score">{cert['score']}</div>
                <div class="cert-rank">Орны: {cert['rank']}-орын</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      # Қай сұрақтан қате кеткені көрініп тұратын бөлім
      if st.session_state.review_result:
        st.subheader("📋 Сіздің жауаптарыңыз бен қателерді талдау:")
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

      if st.button("🚪 Жүйеден шығу (Logout)"):
        st.session_state.logged_user = None
        st.session_state.last_cert = None
        st.session_state.review_result = None
        st.session_state.selected_exam_subject = None
        st.rerun()

    else:
      if not st.session_state.selected_exam_subject:
        st.subheader("🎯 Пәнді таңдаңыз")
        sub = st.selectbox("Пән:", list(st.session_state.questions.keys()))
        if st.button("Тестті бастау"):
          st.session_state.selected_exam_subject = sub
          st.rerun()
      else:
        subject = st.session_state.selected_exam_subject
        q_list = st.session_state.questions[subject]

        if not q_list:
          st.warning("Бұл пөнде сұрақтар жоқ!")
          if st.button("Басқа пән таңдау"):
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
            opts = [f"{k}) {v}" for k, v in q["options"].items() if v.strip()]
            ans = st.radio("Жауапты таңдаңыз:", opts, key=f"ans_{i}")
            user_answers[i] = [ans[0]]

          if st.button("🚀 Тестті аяқтау"):
            score = 0
            review_data = []

            for i, q in enumerate(q_list):
              u_ans = set(user_answers.get(i, []))
              c_ans = set(q["correct"])
              is_corr = u_ans == c_ans and len(u_ans) > 0

              if is_corr:
                score += 1

              review_data.append(
                  {
                      "q_num": i + 1,
                      "question": q["q"],
                      "user_ans": list(u_ans),
                      "correct_ans": list(c_ans),
                      "is_correct": is_corr,
                  }
              )

            total = len(q_list)
            st.session_state.last_cert = {
                "user_fullname": full_name,
                "subject": subject,
                "score": f"{score} / {total}",
                "rank": 1,
            }
            st.session_state.review_result = review_data
            save_data()
            st.rerun()
