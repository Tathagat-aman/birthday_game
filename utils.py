# birthday_game/utils.py
from PIL import Image, ImageFilter
from langchain_groq import ChatGroq
import random
import os
import streamlit as st
GROQ_KEY = st.secrets["GROQ_KEY"]

# Load Groq LLM safely

llm = None
if GROQ_KEY:
    llm = ChatGroq(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        temperature=0.5,
        groq_api_key=GROQ_KEY,
    )

# Local fallback for GenAI response
funny_responses = [
    "😢 Oh no! Did you forget our special moment already? Try again or I’ll cry like a baby panda! 🐼",
    "😭 This answer hurt my virtual heart! You better make it right!",
    "💔 Shivani is disappointed... Just kidding! Try once more and win my heart again! 😘",
    "🥺 Wrong answer... are you testing me or do you not love me anymore?! 😂"
]

def get_llm_response(prompt):
    if llm:
        response = llm.invoke(prompt)
        return response.content.strip()
    return random.choice(funny_responses)

def get_llm_reaction(question):
    # Use a cute funny tone when answer is wrong
    prompt = f"Write a short, funny and emotional reaction for a wrong answer to the question: '{question}'. Make it sound like a cartoon character is crying and teasing."
    return get_llm_response(prompt)

def generate_poem(name):
    prompt = f"Write a short romantic and poetic birthday message for a girl named {name}. Make it playful and emotional, max 6 lines."
    return get_llm_response(prompt), ""

def cartoonify_image(path):
    try:
        img = Image.open(path).convert("RGB")
        img = img.filter(ImageFilter.CONTOUR)
        img = img.filter(ImageFilter.SMOOTH_MORE)
        return img
    except:
        return None

def cartoonify_multiple_images(folder):
    results = []
    for fname in os.listdir(folder):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(folder, fname)
            cartoon = cartoonify_image(path)
            if cartoon:
                results.append((fname, cartoon))
    return results

def generate_gift_description():
    prompt = "Imagine a virtual romantic gift for a girlfriend's birthday (like a flying heart, magical cake, hugging teddy, etc.). Describe it in a short cute sentence with emoji."
    return get_llm_response(prompt)

