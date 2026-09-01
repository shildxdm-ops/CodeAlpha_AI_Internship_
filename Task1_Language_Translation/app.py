import streamlit as st
from deep_translator import GoogleTranslator

# Page configuration
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)

# Title
st.title("🌐 AI Language Translator")
st.write("Translate text easily between different languages.")

# Supported languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru"
}

# Language selection
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

# Text input
text = st.text_area(
    "Enter text to translate:",
    height=150,
    placeholder="Type your text here..."
)

# Translate button
if st.button("🔄 Translate", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text first.")

    elif source_language == target_language:
        st.info("Source and target languages are the same.")

    else:
        try:
            translated_text = GoogleTranslator(
                source=languages[source_language],
                target=languages[target_language]
            ).translate(text)

            st.success("Translation completed!")

            st.subheader("Translated Text")
            st.text_area(
                "Result:",
                translated_text,
                height=150
            )

            # Copyable result
            st.code(translated_text)

        except Exception as e:
            st.error(
                "Translation failed. Please check your internet connection "
                "and try again."
            )