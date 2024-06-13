import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import pyttsx3

# Function to transcribe voice input to text
def transcribe_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something...")
        audio_data = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand your audio.")
        return ""
    except sr.RequestError:
        st.write("Sorry, there was an error processing your request.")
        return ""

# Function to translate text
def translate_text(text, source_lang, target_lang):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src=source_lang, dest=target_lang)
        return translated_text.text
    except Exception as e:
        st.write("Error in translation:", e)
        return ""

# Function to convert text to speech
def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file
    except Exception as e:
        st.write("Error in text-to-speech conversion:", e)
        return None

# Function to speak text
def speak_text(text, lang):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Adjust the speaking rate as needed
        
        # Set the voice based on the language code
        voices = engine.getProperty('voices')
        for voice in voices:
            if lang in voice.languages or lang in voice.id:
                engine.setProperty('voice', voice.id)
                break
        
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.write("Error in speaking text:", e)

# Streamlit UI
st.title("Real-Time Translator")

# Language dictionary
language_dict = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian', 'az': 'Azerbaijani', 
    'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan', 
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)', 
    'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 
    'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole', 
    'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 
    'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 
    'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean', 
    'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 
    'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 
    'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 
    'or': 'Odia', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian', 
    'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 
    'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish', 
    'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu', 
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek', 
    'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}

# Get language names and codes for dropdown
languages = [f"{lang_name} - {lang_code}" for lang_code, lang_name in language_dict.items()]

# Select input and output languages
input_lang = st.selectbox("Select input language:", languages)
output_lang = st.selectbox("Select output language:", languages)

# Extract language codes from dropdown selections
input_lang_code = input_lang.split(" - ")[-1]
output_lang_code = output_lang.split(" - ")[-1]

# Voice input
if st.button("Speak"):
    input_text = transcribe_voice()
    if input_text:
        st.write("Input Text:")
        st.write(input_text)

        # Translate text
        translated_text = translate_text(input_text, input_lang_code, output_lang_code)
        if translated_text:
            st.write("Translated Text:")
            st.write(translated_text)

            # Speak translated text
            st.write("Translated Audio:")
            audio_file = text_to_speech(translated_text, output_lang_code)
            if audio_file:
                st.audio(audio_file)

            # Speak translated text automatically
            speak_text(translated_text, output_lang_code)
