import streamlit as st
import openai
import requests
from io import BytesIO
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="AI Prompt Refiner – klikany", layout="centered")
st.title("🖱️ AI Prompt Refiner z klikaniem")

# 🔑 Ręczne wprowadzanie klucza
api_key = st.text_input("🔑 Wklej swój OpenAI API Key", type="password")

# ✏️ Prompt użytkownika
prompt = st.text_input("✏️ Twój prompt:", value="butelka e-liquidu w stylu zen")

image_url = None

# 🎨 Generowanie obrazu
if st.button("🎨 Wygeneruj obraz"):
    if prompt and api_key:
        openai.api_key = api_key
        with st.spinner("Generuję obraz..."):
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                image_url = response.data[0].url
                st.session_state["image_url"] = image_url
            except Exception as e:
                st.error(f"Błąd: {str(e)}")
    else:
        st.warning("Uzupełnij prompt i klucz API.")

# 🖼️ Wyświetlenie i zaznaczanie
image_url = st.session_state.get("image_url", None)

if image_url:
    # Pobierz i załaduj obraz jako PIL
    try:
        response = requests.get(image_url)
        background_image = Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Nie udało się załadować obrazu: {e}")
        background_image = None

    if background_image:
        st.image(background_image, caption="Kliknij, aby zaznaczyć elementy")

        # Canvas z tłem
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=3,
            stroke_color="#ff0000",
            background_image=background_image,
            update_streamlit=True,
            height=1024,
            width=1024,
            drawing_mode="point",
            key="canvas",
        )

        points = canvas_result.json_data["objects"] if canvas_result.json_data else []

        komentarze = []
        if points:
            st.subheader("💬 Komentarze do zaznaczonych punktów:")
            for i, punkt in enumerate(points):
                komentarz = st.text_input(f"Punkt {i+1} – opis:", key=f"komentarz_{i}")
                komentarze.append(komentarz)

        if st.button("♻️ Wygeneruj nowy prompt"):
            if komentarze:
                nowy_prompt = prompt + ". " + ". ".join(komentarze)
                st.markdown("🆕 **Nowy prompt:**")
                st.code(nowy_prompt)
            else:
                st.info("Dodaj komentarze, aby stworzyć nowy prompt.")
