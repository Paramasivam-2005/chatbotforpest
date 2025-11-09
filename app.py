import streamlit as st
import sys, os, locale
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.inference import identify_pest
from utils.translator import translate
from utils.voice_assistant import speak_text

st.set_page_config(page_title="Pest Identification Assistant", layout="wide")
st.title("🌾 Pest Identification Assistant — Multilingual TTS")

# auto-detect language
try:
    default_lang = locale.getdefaultlocale()[0][:2]
except Exception:
    default_lang = 'en'
if default_lang not in ['en','hi','ta','te','kn']:
    default_lang = 'en'

lang = st.sidebar.selectbox("Language", ['en','hi','ta','te','kn'], index=['en','hi','ta','te','kn'].index(default_lang))
st.sidebar.markdown("""_Language sets both text and audio output._""")

tab1, tab2 = st.tabs(["🪳 Pest Identification", "💬 Chat Assistant"])

with tab1:
    st.header(translate("Pest Identification", lang))
    uploaded = st.file_uploader(translate("Upload image (jpg, png)", lang), type=['jpg','jpeg','png'], key='img')
    col1, col2 = st.columns([1,2])
    with col1:
        if st.button('Load demo image'):
            demo_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test', 'sample.jpg')
            uploaded = open(demo_path, 'rb')
    if uploaded is not None:
        st.image(uploaded, caption=translate('Uploaded image', lang), use_column_width=True)
        with st.spinner(translate('Analyzing...', lang)):
            pest, preds, action_en = identify_pest(uploaded)
        action_trans = translate(action_en, lang)
        out_text = f"Predicted Pest: {pest}. Suggested Action: {action_trans}"
        st.markdown(f"### ✅ {translate('Predicted Pest:', lang)} {translate(pest, lang)}")
        st.markdown("### 📊 " + translate('Confidence scores:', lang))
        st.bar_chart(preds)
        st.markdown(f"### {translate('Suggested Control Action:', lang)}")
        st.success(action_trans)
        # speak in selected language
        audio_path = speak_text(out_text, lang=lang)
        if audio_path:
            st.audio(audio_path, format='audio/mp3')
    else:
        st.info(translate("Please upload an image to identify the pest.", lang))

with tab2:
    st.header(translate("Chat Assistant", lang))
    st.markdown(translate("Type symptoms or ask a question and press Ask.", lang))
    user_text = st.text_input(translate("You:", lang))
    if st.button(translate("Ask", lang)):
        if user_text:
            st.write(translate(f"You asked: {user_text}", lang))
            key = user_text.lower()
            if 'sticky' in key or 'curl' in key or 'honeydew' in key:
                pest = 'Aphid'
            elif 'holes' in key or 'stem' in key:
                pest = 'Stem Borer'
            elif 'white' in key or 'underside' in key:
                pest = 'Whitefly'
            else:
                pest = 'Thrips'
            preds = {pest: 0.85}
            with open(os.path.join(os.path.dirname(__file__), '..', 'utils', 'actions.json')) as f:
                import json
                acts = json.load(f)
                action_en = acts.get(pest, 'Consult local extension.')
            action_trans = translate(action_en, lang)
            st.markdown(f"### {translate('Predicted Pest:', lang)} {translate(pest, lang)}")
            st.markdown(f"### {translate('Suggested Control Action:', lang)}")
            st.success(action_trans)
            # Speak chatbot reply in selected language
            audio_path = speak_text(f"Predicted pest {pest}. Suggested action: {action_trans}", lang=lang)
            if audio_path:
                st.audio(audio_path, format='audio/mp3')
