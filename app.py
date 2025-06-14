import streamlit as st
import openai

st.set_page_config(page_title="AI Prompt Refiner", layout="centered")
st.title("🔁 AI Prompt Refiner – wersja demo")

api_key = st.text_input("🔑 Wklej swój OpenAI API Key", type="password")
prompt = st.text_input("✏️ Twój prompt (np. butelka e-liquidu w stylu zen):")

# PRZYCISK: generuj pierwszy obraz
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

            st.markdown("---")
            st.subheader("🔧 Co chcesz zmodyfikować w tym obrazie?")

            # PRZYKŁADOWE CECHY OBRAZU DO ZAZNACZENIA
            tlo = st.checkbox("🟩 Tło (ciemne)")
            obiekt = st.checkbox("🧴 Butelka")
            styl = st.checkbox("🧘‍♀️ Styl zen")
            tekst = st.checkbox("🔤 Tekst na etykiecie")

            if st.button("♻️ Wygeneruj nowy prompt"):
                zmiany = []
                if tlo: zmiany.append("zmień tło")
                if obiekt: zmiany.append("zmień wygląd butelki")
                if styl: zmiany.append("zmień styl z zen na inny")
                if tekst: zmiany.append("usuń tekst z etykiety")

                if zmiany:
                    nowy_prompt = prompt + ". " + ". ".join(zmiany)
                    st.markdown("🆕 **Nowy prompt:**")
                    st.code(nowy_prompt)
                else:
                    st.info("Zaznacz, co chcesz zmienić.")
    else:
        st.warning("Uzupełnij prompt i klucz API.")
