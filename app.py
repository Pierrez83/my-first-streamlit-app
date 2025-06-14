import streamlit as st
import openai

st.set_page_config(page_title="AI Obraz", layout="centered")
st.title("🧠 Generowanie obrazu AI")

openai.api_key = st.text_input("🔑 Wklej swój OpenAI API Key", type="password")

prompt = st.text_input("✏️ Wpisz prompt (np. butelka e-liquidu w stylu zen):")

if st.button("🎨 Generuj obraz"):
    if prompt and openai.api_key:
        with st.spinner("Generuję obraz..."):
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = response["data"][0]["url"]
            st.image(image_url, caption="Wygenerowany obraz")
    else:
        st.warning("Podaj zarówno prompt, jak i klucz API.")
