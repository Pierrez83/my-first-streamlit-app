import streamlit as st
from PIL import Image
import os

# --- Page Config ---
st.set_page_config(page_title="AI Prompt Refiner", layout="centered")

# --- Session State Init ---
if "image_generated" not in st.session_state:
    st.session_state.image_generated = False

# --- Title & Steps ---
st.markdown("""
### 🧠 Step 1: Create   
🔒 Step 2: Modify   
🔒 Step 3: Refine
---
""")

# --- Prompt Form ---
with st.form("prompt_form"):
    prompt = st.text_area("Describe your idea:", placeholder="e.g. A peaceful garden with misty mountains...")

    format = st.radio("Select format:", options=["3:2", "1:1", "2:3"], horizontal=True)

    style = st.radio("Select style:", options=[
        "Illustration", "Etching", "Photography", "Render", "Oil painting", "Watercolor"
    ], horizontal=True)

    # --- Dynamic Color Pickers ---
if "colors" not in st.session_state:
    st.session_state.colors = ["#7F4A4A", "#4A7F4A", "#FFFFFF"]

st.markdown("**Select main colors:**")
for i, color in enumerate(st.session_state.colors):
    cols = st.columns([0.15, 0.85])
    with cols[0]:
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.colors.pop(i)
            st.experimental_rerun()
    with cols[1]:
        new_color = st.color_picker("", color, key=f"color_{i}", label_visibility="collapsed")
        st.session_state.colors[i] = new_color

if st.button("➕ Add color"):
    st.session_state.colors.append("#FFFFFF")


    use_sample = st.checkbox("Use sample image instead of generating with API")

    submitted = st.form_submit_button("🧠 Generate image")

# --- Image Display ---
st.markdown("""
### 🔍 Generated preview
""")

if submitted:
    if use_sample:
        try:
            image = Image.open("sample.jpg")
            st.image(image, caption="Sample image", use_container_width=True)
            st.session_state.image_generated = True
        except FileNotFoundError:
            st.warning("Sample image not found.")
    else:
        st.warning("API image generation is disabled in this version.")

# --- Step Unlock Display ---
if st.session_state.image_generated:
    st.success("Step 1 complete. You can now continue to Step 2 and Step 3!")
    st.markdown("""
### ✅ Step 2: Modify
### ✅ Step 3: Refine
""")
