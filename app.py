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
if "use_uploaded_photo" not in st.session_state:
    st.session_state.use_uploaded_photo = False

# --- Step Header ---
st.markdown("""
### 🧪 Step 1: Choose Packaging Type  
🔒 Step 2: Adjust Camera Angle  
🔒 Step 3: Upload Label & Generate
---
""")

# --- Step 1: Choose Packaging Type ---
st.markdown("#### 🧴 Select a packaging type or upload your own product photo:")

# Option to upload a photo instead of selecting packaging
st.session_state.use_uploaded_photo = st.checkbox("I already have a photo of the product")

if st.session_state.use_uploaded_photo:
    uploaded_file = st.file_uploader("Upload your product image (JPG or PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded image", use_column_width=True)
        if st.button("Use this as mockup ➡️"):
            st.session_state.step = 3
            st.experimental_rerun()
else:
    package_options = ["Box", "Bottle", "Jar", "Pouch"]
    st.session_state.package_type = st.selectbox("Packaging Type", package_options, index=1)

    # Display placeholder image based on selected package type
    type_to_image = {
        "Box": "images/box_front.png",
        "Bottle": "images/bottle_front.png",
        "Jar": "images/jar_front.png",
        "Pouch": "images/pouch_front.png"
    }

    if st.session_state.package_type in type_to_image:
        try:
            st.image(type_to_image[st.session_state.package_type], width=200, caption="Preview")
        except:
            st.warning("Preview image not found.")

    # Show horizontal angle slider under the preview
    st.session_state.angle_horizontal = st.slider(
        "Rotate product left ↔ right", min_value=-90, max_value=90, value=0, step=15, key="horizontal_slider")

    # Show vertical angle slider on the right
    with st.container():
        cols = st.columns([5, 1])
        with cols[1]:
            st.session_state.angle_vertical = st.slider(
                "Tilt up/down", min_value=0, max_value=90, value=0, step=15, key="vertical_slider", label_visibility="collapsed")

    # Proceed button
    if st.button("Next ➡️", key="to_step3"):
        st.session_state.step = 3
        st.experimental_rerun()

# --- Placeholder for Step 3 ---
if st.session_state.step == 3:
    st.markdown("""
    ### 🎨 Step 3: Upload Label & Generate
    (Coming soon...)
    """)
