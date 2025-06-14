import streamlit as st
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="AI Product Mockup", layout="centered")

# --- Session State Init ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "package_type" not in st.session_state:
    st.session_state.package_type = "Bottle"
if "angle_horizontal" not in st.session_state:
    st.session_state.angle_horizontal = 0
if "angle_vertical" not in st.session_state:
    st.session_state.angle_vertical = 0

# --- Step Header ---
st.markdown("""
### 🧪 Step 1: Choose Packaging Type  
🔒 Step 2: Adjust Camera Angle  
🔒 Step 3: Upload Label & Generate
---
""")

# --- Step 1: Choose Packaging Type ---
st.markdown("#### 🧴 Select a packaging type:")
package_options = ["Box", "Bottle", "Jar", "Pouch"]
st.session_state.package_type = st.selectbox("Packaging Type", package_options, index=1)

if st.button("Next ➡️", key="to_step2"):
    st.session_state.step = 2
    st.experimental_rerun()

# --- Step 2: Adjust Camera Angle ---
if st.session_state.step >= 2:
    st.markdown("""
    ### 🎥 Step 2: Set Camera Angle
    Adjust how the camera views your product.
    """)

    st.session_state.angle_horizontal = st.slider("Horizontal angle (left ↔ right)", min_value=0, max_value=180, value=0, step=15)
    st.session_state.angle_vertical = st.slider("Vertical angle (top ↕ bottom)", min_value=0, max_value=90, value=0, step=15)

    st.markdown(f"**Selected angle:** {st.session_state.angle_horizontal}° horizontal / {st.session_state.angle_vertical}° vertical")

    if st.button("Next ➡️", key="to_step3"):
        st.session_state.step = 3
        st.experimental_rerun()

# --- Placeholder for Step 3 ---
if st.session_state.step == 3:
    st.markdown("""
    ### 🎨 Step 3: Upload Label & Generate
    (Coming soon...)
    """)
