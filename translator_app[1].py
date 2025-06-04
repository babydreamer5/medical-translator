
import streamlit as st
import speech_recognition as sr
import openai
from gtts import gTTS
import os
import tempfile

# OpenAI API 키 입력
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎙️ 진료 중 실시간 영어 통역기")
st.write("버튼을 눌러 말씀하시면, 자동으로 영어로 번역됩니다.")

if st.button("🎤 녹음 시작"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("듣고 있어요. 말씀해 주세요...")
        audio = recognizer.listen(source)

    try:
        korean_text = recognizer.recognize_google(audio, language="ko-KR")
        st.success(f"🗣️ 인식된 한국어: {korean_text}")

        messages = [
            {"role": "system", "content": "You are a medical interpreter. Translate Korean to English for doctor-patient communication."},
            {"role": "user", "content": korean_text}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        english_translation = response.choices[0].message.content.strip()
        st.success(f"🇺🇸 영어 번역: {english_translation}")

        tts = gTTS(english_translation, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")

    except Exception as e:
        st.error(f"문제가 발생했어요: {str(e)}")
