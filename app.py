import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Visual Prompt Tool", layout="centered")

# --- Header navigation ---
st.markdown("""
### 🧠 Step 1: Create &nbsp;&nbsp;&nbsp;&nbsp;🔒 Step 2: Modify &nbsp;&nbsp;&nbsp;&nbsp;🔒 Step 3: Refine
""")

st.markdown("---")

# --- Prompt input ---
prompt = st.text_area("Describe your idea:", placeholder="e.g. A peaceful garden with misty mountains...", height=100)

# --- Format selection ---
st.markdown("**Select format:**")
formats = ["3:2", "1:1", "2:3"]
selected_format = st.radio("", formats, horizontal=True, label_visibility="collapsed")

# --- Style selection ---
st.markdown("**Select style:**")
styles = ["Illustration", "Etching", "Photography", "Render", "Oil painting", "Watercolor"]
selected_style = st.radio("", styles, horizontal=True, label_visibility="collapsed")

# --- Color selection ---
st.markdown("**Select main colors:**")
color_col1, color_col2 = st.columns([6, 1])

if 'colors' not in st.session_state:
    st.session_state.colors = []

with color_col1:
    for idx, color in enumerate(st.session_state.colors):
        col = st.color_picker("", color, label_visibility="collapsed", key=f"cp_{idx}")
        st.session_state.colors[idx] = col

with color_col2:
    if st.button("➕"):
        st.session_state.colors.append("#ffffff")

# --- Generate button ---
st.markdown("---")
generate = st.button("🎨 Generate image")

# --- Output ---
if generate:
    st.subheader("🔍 Generated preview")
    image_path = "Zrzut ekranu 2025-06-14 o 17.03.10.png"
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, use_column_width=True)
    else:
        st.warning("Sample image not found.")
