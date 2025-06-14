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
if "angle_rotation" not in st.session_state:
    st.session_state.angle_rotation = 0

# --- Step Header ---
st.markdown("""
### 🧪 Step 1: Choose Packaging Type  
🔒 Step 2: Adjust Camera Angle  
🔒 Step 3: Upload Label & Generate
---
""")

# --- Step 1: Packaging Selection ---
st.markdown("#### 🧴 Select a packaging type:")
package_options = ["Box", "Bottle", "Jar", "Pouch"]
st.session_state.package_type = st.selectbox("Packaging Type", package_options, index=1)

# --- Image Preview ---
type_to_image = {
    "Box": "images/box_front.png",
    "Bottle": "images/bottle_front.png",
    "Jar": "images/jar_front.png",
    "Pouch": "images/pouch_front.png"
}
if st.session_state.package_type in type_to_image:
    try:
        st.image(type_to_image[st.session_state.package_type], width=250, caption="Preview")
    except:
        st.warning("Preview image not found.")

# --- Sliders Layout ---
st.divider()
st.markdown("### 🎛️ Adjust Camera Angles:")

# Horizontal rotation (left ↔ right)
st.session_state.angle_horizontal = st.slider(
    "🌀 Rotate product (left/right)", min_value=-180, max_value=180, value=0, step=15)

# Vertical tilt (camera up/down)
cols = st.columns([5, 1])
with cols[1]:
    st.session_state.angle_vertical = st.slider(
        "🔼🔽 Tilt camera (up/down)", min_value=-90, max_value=90, value=0, step=15,
        label_visibility="collapsed")

# Rotation around vertical axis (roll)
st.session_state.angle_rotation = st.slider(
    "🔁 Rotate around product axis (e.g. twist bottle)", min_value=-180, max_value=180, value=0, step=15)

# --- Proceed ---
if st.button("Next ➡️", key="to_step3"):
    st.session_state.step = 3
    st.experimental_rerun()

# --- Step 3 Placeholder ---
if st.session_state.step == 3:
    st.markdown("""
    ### 🎨 Step 3: Upload Label & Generate
    (Coming soon...)
    """)
