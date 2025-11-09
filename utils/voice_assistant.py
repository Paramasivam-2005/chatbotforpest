import os, tempfile
def speak_text(text, lang='en'):
    """Speak text and return path to audio file if created (mp3) for Streamlit playback.
    Tries pyttsx3 for offline English; otherwise uses gTTS (requires internet) for any lang.
    Returns path to mp3 file or None if pyttsx3 handled speaking inline."""
    # Try pyttsx3 for offline English/any if available
    try:
        import pyttsx3
        engine = pyttsx3.init()
        # if language is not English, pyttsx3 voices may not support it; still try for en
        if lang == 'en':
            engine.say(text)
            engine.runAndWait()
            return None
    except Exception:
        pass
    # Fallback to gTTS to synthesize mp3
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang if lang in ['en','hi','ta','te','kn'] else 'en')
        fd, path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
        tts.save(path)
        return path
    except Exception:
        return None
