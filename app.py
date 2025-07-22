import streamlit as st
from sentence_transformers import SentenceTransformer
import torch
import faiss
import numpy as np
import time
import os
import openai
import csv

# --- TRACK USER INTERACTION ---
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 1
else:
    st.session_state.visit_count += 1

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

elapsed_time = time.time() - st.session_state.start_time

st.title("🧴 Smart Cleanser Finder")
st.write(f"Visit count: {st.session_state.visit_count}")
st.write(f"Time on page: {int(elapsed_time)} seconds")

# --- USER NATURAL LANGUAGE OPTION ---
user_text = st.text_input("Tell me your skin type or skin concern:")
skin_type, skin_concern, budget = None, None, None
if user_text:
    if "dry" in user_text.lower(): skin_type = "Dry"
    elif "oily" in user_text.lower(): skin_type = "Oily"
    elif "combo" in user_text.lower(): skin_type = "Combination"

    if "red" in user_text.lower(): skin_concern = "Redness"
    elif "acne" in user_text.lower(): skin_concern = "Acne"
    elif "sensitive" in user_text.lower(): skin_concern = "Sensitivity"

    budget = 20  # placeholder if mentioned, can be enhanced

# --- FORM INPUT FALLBACK ---
st.subheader("🧼 Get a Personalized Cleanser Match")
skin_type = st.selectbox("What is your skin type?", ["Oily", "Dry", "Combination"])
skin_concern = st.selectbox("What is your main concern?", ["Redness", "Acne", "Sensitivity"])
budget = st.slider("What is your budget range?", 5, 30, 15)

if st.button("Get Recommendations"):
    st.write("🔍 Searching for best matches...")

    cleansers = [
        {"name": "La Roche-Posay Toleriane Cleanser", "description": "Gentle on redness, good for sensitive combo skin.", "price": "$14.99", "url": "https://example.com/la-roche"},
        {"name": "COSRX Low pH Gel Cleanser", "description": "Tea tree and BHA for oily or acne-prone skin. pH balanced.", "price": "$11.99", "url": "https://example.com/cosrx"},
        {"name": "Vanicream Gentle Cleanser", "description": "No fragrance or sulfates. Ideal for allergy-prone users.", "price": "$9.50", "url": "https://example.com/vanicream"}
    ]

    for product in cleansers:
        st.success(product["name"])
        st.write(product["description"])
        st.write(f"Price: {product['price']}")
        st.markdown(f"[Buy now]({product['url']})")
        st.caption(f"Matched for: {skin_type}, Concern: {skin_concern}, Budget: under ${budget}")

    # --- FEEDBACK ---
    feedback = st.radio("Was this recommendation helpful?", ["👍 Yes", "👎 No"])
    if feedback:
        st.write("Thanks for your feedback!")

    # --- AUDIT LOGGING ---
    log_data = {
        "skin_type": skin_type,
        "concern": skin_concern,
        "budget": budget,
        "recommendations": [p["name"] for p in cleansers],
        "feedback": feedback
    }

    with open("audit_log.csv", mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=log_data.keys())
        writer.writerow(log_data)
