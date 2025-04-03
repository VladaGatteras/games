import streamlit as st
import random
import base64
import logging
import os

st.set_page_config(page_title="Квест Дня Рождения",
                   page_icon="🎂", layout="wide")

# --- Настройка логов ---
log_path = os.path.join(os.path.dirname(__file__), "birthday_quest.log")
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# --- Фон ---


def set_background_from_file(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            html, body, .stApp {{
                height: 100%;
                margin: 0;
                padding: 0;
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                overflow-x: hidden;
            }}
            .block-container {{
                background-color: rgba(255, 255, 255, 0.85);
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
            }}
            .char-container {{
                text-align: center;
            }}
            /* Отступ сверху для картинок персонажей */
            .char-container img {{
                margin-top: 1em;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error("Ошибка загрузки фона")
        logging.error(f"Ошибка при загрузке фона: {e}")


set_background_from_file("image.png")

# --- Данные: персонажи и вопросы ---
characters = [
    {
        "name": "Босс отдела",
        "image": "Босс отдела.png",
        "questions": [
            {
                "question": "Что всегда делает наш босс?",
                "options": ["Говорит 'срочно'", "Пьёт чай", "Пишет отчёты", "Опаздывает"],
                "answer": "Говорит 'срочно'"
            },
            {
                "question": "Какое у него супероружие?",
                "options": ["Письма в Outlook", "Excel-таблицы", "Сила взгляда", "Контроль дедлайна"],
                "answer": "Контроль дедлайна"
            }
        ]
    },
    {
        "name": "Алина",
        "image": "Алина.png",
        "questions": [
            {
                "question": "Что любит Алина?",
                "options": ["Дизайн", "Чат GPT", "Шоколад", "Мемы про котиков"],
                "answer": "Мемы про котиков"
            },
            {
                "question": "Какую фразу она говорит чаще всего?",
                "options": ["Я уже почти закончила", "Это можно в Notion", "Ща залью в Фигму", "Ой, это не финал"],
                "answer": "Ща залью в Фигму"
            }
        ]
    },
    {"name": "Персонаж ещё не раскрыт", "image": "Третий.png", "questions": []},
    {"name": "Персонаж ещё не раскрыт", "image": "Четвёртый.png", "questions": []},
    {"name": "Персонаж ещё не раскрыт", "image": "Пятый.png", "questions": []},
    {"name": "Персонаж ещё не раскрыт", "image": "Шестой.png", "questions": []}
]

# --- Функции-колбэки ---


def select_character(index):
    st.session_state.character = characters[index]
    st.session_state.stage = 0
    st.session_state.correct = 0


def check_answer():
    char = st.session_state.character
    stage = st.session_state.stage
    q = char["questions"][stage]
    selected = st.session_state.get(f"q{stage}")
    if selected == q["answer"]:
        st.session_state.correct += 1
        st.session_state.stage += 1
    else:
        st.session_state.error = "Неправильно. Попробуй ещё раз."

# --- Интерфейс ---


# Отступ сверху для заголовочного ряда
st.markdown("<br>", unsafe_allow_html=True)

# Заголовочный ряд с изображением head.png
header_cols = st.columns(7)
with header_cols[3]:
    st.image("head.png", width=300)

# Инструкция под заголовком, по центру
instr_cols = st.columns(3)
with instr_cols[1]:
    st.markdown(
        "<p style='text-align: center; font-size: 20px;'>Нажми кнопку <strong>Выбрать</strong>, чтобы начать!</p>",
        unsafe_allow_html=True,
    )

# Если персонаж ещё не выбран – показываем ряд с персонажами
if "character" not in st.session_state:
    char_cols = st.columns(len(characters))
    for i, char in enumerate(characters):
        with char_cols[i]:
            with open(char['image'], "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f"""
                <div class="char-container">
                    <img src="data:image/png;base64,{img_data}" width="120">
                    <p><strong>{char['name']}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col_left, col_center, col_right = st.columns([1, 2, 1])
            with col_center:
                st.button(
                    "Выбрать", key=f"select_{i}", on_click=select_character, args=(i,))
# Если персонаж выбран – показываем вопросы
else:
    char = st.session_state.character
    st.subheader(f"Ты выбрал: {char['name']}")
    if len(char.get("questions", [])) > 0 and st.session_state.stage < len(char["questions"]):
        stage = st.session_state.stage
        q = char["questions"][stage]
        st.subheader(f"Вопрос {stage + 1}: {q['question']}")
        st.radio("Выбери ответ:", q["options"], key=f"q{stage}")
        st.button("Ответить", key=f"submit_{stage}", on_click=check_answer)
        if "error" in st.session_state:
            st.error(st.session_state.error)
            del st.session_state.error
    else:
        st.subheader("🎉 Квест завершён!")
        st.markdown(f"**Ты прошёл путь с персонажем:** {char['name']}")
        st.markdown("---")
        st.markdown("### 🎁 Поддержи подарок имениннику:")
        st.markdown(
            "**💸 Ссылка для перевода:** [Перевести](https://your-donation-link.com)")
        st.markdown("**📱 По номеру телефона:** +7-999-123-4567")
        if st.button("Я задонатил! Открыть бонус персонажа"):
            bonus = random.choice([
                {"name": "Золотой Донатор", "class": "Герой офиса",
                    "power": "Призывает идеальные подарки"},
                {"name": "Страж Праздника", "class": "Танк настроения",
                    "power": "Защищает веселье от дедлайнов"}
            ])
            st.balloons()
            st.success("Ты разблокировал бонусного героя!")
            st.markdown(
                f"🌟 **{bonus['name']}**\n\nКласс: *{bonus['class']}*\n\nСпецспособность: `{bonus['power']}`")
        if st.button("Пройти заново"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
