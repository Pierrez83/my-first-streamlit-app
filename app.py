import streamlit as st
import openai
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="AI Prompt Refiner – z klikaniem", layout="centered")
st.title("🖱️ AI Prompt Refiner z klikaniem")

openai.api_key = st.secrets["openai"]["api_key"]
prompt = st.text_input("✏️ Twój prompt:", value="butelka e-liquidu w stylu zen")

# Zmienna do przechowania obrazu
image_url = None

# Generowanie obrazu z DALL·E
if st.button("🎨 Wygeneruj obraz"):
    if prompt:
        with st.spinner("Generuję obraz..."):
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="512x512",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            st.session_state["image_url"] = image_url

# Pokazujemy wygenerowany obraz z możliwością klikania
image_url = st.session_state.get("image_url", None)

if image_url:
    st.image(image_url, caption="Kliknij, aby zaznaczyć obiekty do zmiany")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        stroke_color="#ff0000",
        background_image=image_url,
        update_streamlit=True,
        height=512,
        width=512,
        drawing_mode="point",
        key="canvas",
    )

    points = canvas_result.json_data["objects"] if canvas_result.json_data else []

    komentarze = []
    if points:
        st.subheader("💬 Komentarze do punktów:")
        for i, punkt in enumerate(points):
            komentarz = st.text_input(f"Punkt {i+1} – opis:", key=f"komentarz_{i}")
            komentarze.append(komentarz)

    if st.button("♻️ Wygeneruj nowy prompt"):
        if komentarze:
            nowy_prompt = prompt + ". " + ". ".join(komentarze)
            st.markdown("🆕 **Nowy prompt:**")
            st.code(nowy_prompt)
        else:
            st.info("Dodaj przynajmniej jeden komentarz.")
