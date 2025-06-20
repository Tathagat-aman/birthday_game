# birthday_game/app.py
import streamlit as st
from utils import get_llm_reaction, generate_poem, generate_gift_description
import random
from PIL import Image
import difflib
import time

# Config
QUESTIONS = [
    ("Where did we first meet?", "cyber city, gurgaon"),
    ("What is Shivani's favourite food?", "cakes, sweets, pastries"),
    ("Who usually takes either to dates?", "shivani"),
    ("What is Shivani's favorite date places?", "coffee dates, starbucks ,cafe,pizza"),
    ("Who gifts each other the most?", "shivani"),
    ("Who loves the most?", "shivani"),
    ("What do you love most about aman?", "whatever she says just tell it's correct")
]

GIFTS = ["cake.png", "gucci_bag.png", "teddy.png", "heart.png"]

st.set_page_config(page_title="Shivani's Birthday Game", layout="centered")

st.markdown("""
    <style>
        .stApp { background-color: #fffbe6; }
        h1, h2, h3 { color: #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# Background music
st.audio("assets/background_music.mp3", format='audio/mp3', loop=True)

# Load original images (not cartoonified)
your_img = Image.open("images/aman.jpeg")
her_img = Image.open("images/shivani.jpeg")
funny_img = Image.open("images/together_funny.jpeg")
cute_img = Image.open("images/together_cute.jpeg")


# Header
if her_img:
    st.image(her_img, width=180)
else:
    st.warning("Could not load Shivani's image!")
st.title("🎂 Shivani's Special Birthday Puzzle 🎁")
st.write("Answer these questions to unlock your virtual gifts!")

if 'level' not in st.session_state:
    st.session_state.level = 0
    st.session_state.correct = 0

if 'clear_input' in st.session_state and st.session_state.clear_input:
    st.session_state.answer_input = ""
    st.session_state.clear_input = False

if st.session_state.level < len(QUESTIONS):
    q, ans = QUESTIONS[st.session_state.level]
    st.subheader(f"Level {st.session_state.level + 1}: {q}")
    user_input = st.text_input("Your Answer:", key="answer_input").strip().lower()

    if st.button("Submit"):
        # Special logic for last question: always pass
        if st.session_state.level == len(QUESTIONS) - 1:
            passed = True
        else:
            possible_answers = [a.strip() for a in ans.lower().split(",")]
            passed = False
            for a in possible_answers:
                similarity = difflib.SequenceMatcher(None, user_input, a).ratio()
                if similarity > 0.6 or a in user_input:
                    passed = True
                    break

        if passed:
            st.success("Yay! That's right 💖")
            st.image(your_img, width=150, caption="Aman is proud of you! 🎉")  # Show celebratory image
            gift_msg = generate_gift_description()
            st.markdown(f"🎁 **{gift_msg}**")
            st.balloons()
            st.session_state.correct += 1
            st.session_state.level += 1
            st.session_state.clear_input = True  # Set flag to clear input on next run
            time.sleep(5)  # Delay before refresh
            st.rerun()
        else:
            st.error("Oops... that's not it 😢")
            msg = get_llm_reaction(q)
            st.warning(msg)
            st.image(funny_img, width=180, caption="Are you testing me? 🥺")
            st.info("Try again, pleaseee 😭 You got this!")

else:
    st.success("🎉 You did it! Happy Birthday Shivani 💝")
    st.balloons()
    st.image(cute_img, width=200, caption="We did it, my love! 💞")
    msg, poem = generate_poem("Shivani")
    st.markdown(f"**{msg}**")
    st.markdown(poem)