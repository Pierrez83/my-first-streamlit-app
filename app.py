import streamlit as st
from PIL import Image
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

    st.markdown("**Lasso tool mockup:**")
    st.session_state.lasso_mode = st.radio("Select lasso mode:", ["Keep (🟢)", "Remove (🔴)"])

    st.file_uploader("Upload a lasso-marked image (mockup only):", type=["jpg", "png"], key="lasso_upload")

    with st.form("lasso_instruction_form"):
        lasso_desc = st.text_area("Describe what the marked area should represent:", placeholder="e.g. Remove the red object in the bottom-left")
        save_instr = st.form_submit_button("➕ Add instruction")
        if save_instr and lasso_desc.strip():
            st.session_state.modifications.append(f"[{st.session_state.lasso_mode}] {lasso_desc.strip()}")

    if st.session_state.modifications:
        st.markdown("#### 📝 Current modifications queue:")
        for mod in st.session_state.modifications:
            st.markdown(f"- {mod}")

    st.markdown("---")
    st.markdown("### 🔒 Step 3: Refine")
