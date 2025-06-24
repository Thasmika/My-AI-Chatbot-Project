import streamlit as st
import openai
import pyttsx3
import speech_recognition as sr
import os

# ------------ SETUP OPENAI API KEY ------------
openai.api_key = "Enter your API KEY"  # 🔁 Replace with your actual API key

# ------------ INITIALIZE TOOLS ------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()
chat_history_file = "chat_history.txt"

# ------------ VOICE FUNCTIONS ------------
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {text}")
            return text
        except:
            st.error("❌ Sorry, I couldn't understand.")
            return ""

# ------------ CHATBOT FUNCTION ------------
def chat_with_gpt(user_input):
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    bot_reply = response.choices[0].message["content"]
    save_chat(user_input, bot_reply)
    return bot_reply

# ------------ SAVE CHAT TO FILE ------------
def save_chat(user_msg, bot_msg):
    with open(chat_history_file, "a", encoding="utf-8") as f:
        f.write(f"\nUser: {user_msg}\nBot: {bot_msg}\n{'-'*30}\n")

# ------------ GUI WITH STREAMLIT ------------
st.set_page_config(page_title="My AI Chatbox", layout="centered", page_icon="🤖")

st.markdown("""
    <h1 style='text-align: center; color: #1F77B4;'>🤖 My AI Chatbox</h1>
    <p style='text-align: center; color: gray;'>Talk with your AI using text or voice!</p>
    <hr style='border: 1px solid #1F77B4;'>
""", unsafe_allow_html=True)

input_mode = st.radio("Select Input Mode:", ["💬 Type Message", "🎤 Voice Input"])

# ------------ INPUT METHODS ------------
if input_mode == "💬 Type Message":
    user_input = st.text_input("Your message:")
    if st.button("Send"):
        if user_input:
            reply = chat_with_gpt(user_input)
            st.success("🤖 Bot: " + reply)
            speak(reply)

elif input_mode == "🎤 Voice Input":
    if st.button("Speak Now"):
        voice_input = listen()
        if voice_input:
            reply = chat_with_gpt(voice_input)
            st.success("🤖 Bot: " + reply)
            speak(reply)

# ------------ CHAT HISTORY VIEWER ------------
if st.button("📜 Show Chat History"):
    if os.path.exists(chat_history_file):
        with open(chat_history_file, "r", encoding="utf-8") as f:
            history = f.read()
            st.text_area("Chat History", history, height=300)
    else:
        st.warning("⚠️ No chat history found yet.")

# ------------ CLEAR CHAT HISTORY ------------
if st.button("🗑️ Clear Chat History"):
    if os.path.exists(chat_history_file):
        os.remove(chat_history_file)
        st.success("✅ Chat history cleared.")
    else:
        st.warning("⚠️ No history to delete.")