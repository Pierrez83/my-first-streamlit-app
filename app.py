import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
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

    st.session_state.lasso_mode = st.radio("Select mode:", ["Keep (🟢)", "Remove (🔴)"])
    desc = st.text_input("Describe selected area:", placeholder="e.g. Remove tree on the left")

    st.markdown("**Draw on image below:**")

    sample_path = "sample.jpg"
    if os.path.exists(sample_path):
        image = Image.open(sample_path)
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)" if "Remove" in st.session_state.lasso_mode else "rgba(0, 255, 0, 0.3)",
            stroke_width=3,
            stroke_color="#ff0000" if "Remove" in st.session_state.lasso_mode else "#00ff00",
            background_image=image,
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="rect",
            key="canvas",
        )

        if st.button("➕ Add drawn selection"):
            if canvas_result.json_data and desc.strip():
                st.session_state.modifications.append(
                    f"[{st.session_state.lasso_mode}] Drawn area – {desc.strip()}"
                )
    else:
        st.warning("sample.jpg not found")

    if st.session_state.modifications:
        st.markdown("#### 📝 Current modifications queue:")
        for mod in st.session_state.modifications:
            st.markdown(f"- {mod}")

    st.markdown("---")
    st.markdown("### 🔒 Step 3: Refine")
