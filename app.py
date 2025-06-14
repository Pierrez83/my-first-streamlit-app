import streamlit as st
from PIL import Image, ImageDraw
import os

# --- Page Config ---
st.set_page_config(page_title="AI Prompt Refiner", layout="centered")

# --- Session State Init ---
if "image_generated" not in st.session_state:
    st.session_state.image_generated = False
if "colors" not in st.session_state:
    st.session_state.colors = ["#7F4A4A", "#4A7F4A", "#FFFFFF"]
if "modifications" not in st.session_state:
    st.session_state.modifications = []
if "lasso_mode" not in st.session_state:
    st.session_state.lasso_mode = "Keep"

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

    use_sample = st.checkbox("Use sample image instead of generating with API")

    submitted = st.form_submit_button("🧠 Generate image")

# --- Color Picker Section (outside form) ---
st.markdown("**Select main colors:**")
i = 0
while i < len(st.session_state.colors):
    cols = st.columns([0.15, 0.85])
    with cols[0]:
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.colors.pop(i)
            st.experimental_rerun()
    with cols[1]:
        new_color = st.color_picker("", st.session_state.colors[i], key=f"color_{i}", label_visibility="collapsed")
        st.session_state.colors[i] = new_color
    i += 1

if st.button("➕ Add color"):
    st.session_state.colors.append("#FFFFFF")
    st.experimental_rerun()

# --- Image Display ---
st.markdown("### 🔍 Generated preview")

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

# --- Step 2: Modify ---
if st.session_state.image_generated:
    st.success("Step 1 complete. You can now continue to Step 2 and Step 3!")

    st.markdown("### ✅ Step 2: Modify")
    st.markdown("*Focus on large structural changes to the image. Details like texture, lighting, or text should be added in Step 3: Refine.*")

    st.markdown("**Mark area directly on sample image (rectangular coordinates):**")
    st.session_state.lasso_mode = st.radio("Select mode:", ["Keep (🟢)", "Remove (🔴)"])

    with st.form("region_selector"):
        x = st.number_input("X (left)", min_value=0, value=0)
        y = st.number_input("Y (top)", min_value=0, value=0)
        width = st.number_input("Width", min_value=1, value=100)
        height = st.number_input("Height", min_value=1, value=100)
        desc = st.text_area("Describe what this selection means:", placeholder="e.g. Remove the tree from the bottom-left")
        confirm = st.form_submit_button("➕ Add region")

    if confirm:
        region_info = f"[{st.session_state.lasso_mode}] Rectangle at ({x},{y},{width},{height}) – {desc.strip()}"
        st.session_state.modifications.append(region_info)

        # Draw rectangle preview (optional)
        try:
            img = Image.open("sample.jpg").convert("RGB")
            draw = ImageDraw.Draw(img)
            color = "green" if "Keep" in st.session_state.lasso_mode else "red"
            draw.rectangle([x, y, x + width, y + height], outline=color, width=4)
            st.image(img, caption="Preview with marked region", use_container_width=True)
        except Exception as e:
            st.warning(f"Preview failed: {e}")

    if st.session_state.modifications:
        st.markdown("#### 📝 Current modifications queue:")
        for mod in st.session_state.modifications:
            st.markdown(f"- {mod}")

    st.markdown("---")
    st.markdown("### 🔒 Step 3: Refine")
