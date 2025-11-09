# Pest Identification Assistant — Multilingual TTS (Final)

Features:
- Image-based pest detection (demo deterministic predictor)
- Pest control suggestions (actions.json)
- Full text translation + audio in English, Hindi, Tamil, Telugu, Kannada (offline mock translations)
- Voice output for both pest results and chatbot replies.
  - Uses pyttsx3 for offline English if available.
  - Falls back to gTTS for other languages or when pyttsx3 is not available (requires internet).
- Tabbed Streamlit UI (Pest Identification | Chat Assistant)
- Demo image and sample questions included.

## How to run (Windows PowerShell)
1. Extract the ZIP.
2. Open PowerShell in the folder.
3. Create and activate env:
   python -m venv env
   .\env\Scripts\Activate.ps1
4. Install requirements:
   pip install -r requirements.txt
5. Run the app:
   streamlit run app/chatbot_ui.py

## Notes
- gTTS requires internet to generate audio. If your demo environment has no internet and pyttsx3 isn't installed, audio will not be available but text will display.
- To integrate your real trained model, replace utils/inference.py with code that loads your model and returns (pest, preds_dict, action_en).
