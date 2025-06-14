import streamlit as st
import openai

st.set_page_config(page_title="AI Obraz", layout="centered")
st.title("🧠 Generowanie obrazu AI")

api_key = st.text_input("🔑 Wklej swój OpenAI API Key", type="password")
prompt = st.text_input("✏️ Wpisz prompt (np. butelka e-liquidu w stylu zen):")

if st.button("🎨 Generuj obraz"):
    if prompt and api_key:
        openai.api_key = api_key
        with st.spinner("Generuję obraz..."):
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
            st.image(image_url, caption="Wygenerowany obraz")
    else:
        st.warning("Podaj zarówno prompt, jak i klucz API.")
