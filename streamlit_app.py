import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
from PIL import Image

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the translator
translator = Translator()

# Language dictionary
language_dict = {
    'afrikaans': 'af',
    'albanian': 'sq',
    'amharic': 'am',
    'arabic': 'ar',
    'armenian': 'hy',
    'azerbaijani': 'az',
    'basque': 'eu',
    'belarusian': 'be',
    'bengali': 'bn',
    'bosnian': 'bs',
    'bulgarian': 'bg',
    'catalan': 'ca',
    'cebuano': 'ceb',
    'chichewa': 'ny',
    'chinese (simplified)': 'zh',
    'chinese (traditional)': 'zh-TW',
    'corsican': 'co',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'esperanto': 'eo',
    'estonian': 'et',
    'filipino': 'tl',
    'finnish': 'fi',
    'french': 'fr',
    'frisian': 'fy',
    'galician': 'gl',
    'georgian': 'ka',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    'haitian creole': 'ht',
    'hausa': 'ha',
    'hawaiian': 'haw',
    'hebrew': 'he',
    'hindi': 'hi',
    'hmong': 'hmn',
    'hungarian': 'hu',
    'icelandic': 'is',
    'igbo': 'ig',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'javanese': 'jv',
    'kannada': 'kn',
    'kazakh': 'kk',
    'khmer': 'km',
    'kinyarwanda': 'rw',
    'korean': 'ko',
    'kurdish': 'ku',
    'kyrgyz': 'ky',
    'lao': 'lo',
    'latin': 'la',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'luxembourgish': 'lb',
    'macedonian': 'mk',
    'malagasy': 'mg',
    'malay': 'ms',
    'malayalam': 'ml',
    'maltese': 'mt',
    'maori': 'mi',
    'marathi': 'mr',
    'mongolian': 'mn',
    'myanmar (burmese)': 'my',
    'nepali': 'ne',
    'norwegian': 'no',
    'odia': 'or',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    'portuguese': 'pt',
    'punjabi': 'pa',
    'romanian': 'ro',
    'russian': 'ru',
    'samoan': 'sm',
    'scots gaelic': 'gd',
    'serbian': 'sr',
    'sesotho': 'st',
    'shona': 'sn',
    'sindhi': 'sd',
    'sinhala': 'si',
    'slovak': 'sk',
    'slovenian': 'sl',
    'somali': 'so',
    'spanish': 'es',
    'sundanese': 'su',
    'swahili': 'sw',
    'swedish': 'sv',
    'tajik': 'tg',
    'tamil': 'ta',
    'telugu': 'te',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'uyghur': 'ug',
    'uzbek': 'uz',
    'vietnamese': 'vi',
    'welsh': 'cy',
    'xhosa': 'xh',
    'yiddish': 'yi',
    'yoruba': 'yo',
    'zulu': 'zu',
}


img=Image.open('finallogo.jpg')

col1, col2 = st.columns([1,3])

with col1:
        st.image(img, width=220)

with col2:
        custom_theme = {
            "theme": {
                "primaryColor": "#000000",
                "backgroundColor": "#89939E",
                "secondaryBackgroundColor": "#262730",
                "textColor": "#FFFFFF",
                "font": "Serif"
            }
        }

        # Apply custom theme to Streamlit
        st.markdown(
            f"""
            <style>
            :root {{
                --primary-color: {custom_theme["theme"]["primaryColor"]};
                --background-color: {custom_theme["theme"]["backgroundColor"]};
                --secondary-background-color: {custom_theme["theme"]["secondaryBackgroundColor"]};
                --text-color: {custom_theme["theme"]["textColor"]};
                --font: {custom_theme["theme"]["font"]};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


        
        st.title("AMPYtranslate")

st.header("")
hide_st_style = """
                <style>
                #Mainmenu{visibility: hidden;}
                footer{visibility:hidden; }
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)


# Function to recognize speech
def recognize_speech(prompt, language='en'):
    try:
        with sr.Microphone() as source:
            st.write(prompt)
            # Use recognizer to adjust to ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
            st.write("Recognizing...")

        # Recognize the speech in the specified language
        spoken_text = recognizer.recognize_google(audio, language=language)
        return spoken_text
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand your speech.")

        

# Function to translate speech
def translate_speech():
    # Get source language name and convert it to code
    source_language_name = recognize_speech("Please speak the source language name (e.g., 'English'): ")
    source_language = language_dict.get(source_language_name.lower(), 'en')

    # Get sentence to translate
    sentence = recognize_speech("Please speak the sentence to translate:", language=source_language)
    while sentence is None:
        sentence = recognize_speech("Please speak the sentence to translate:", language=source_language)

    # Get destination language name and convert it to code
    destination_language_name = recognize_speech("Please speak the destination language name (e.g., 'French'): ")
    destination_language = language_dict.get(destination_language_name.lower(), 'en')

    # Translate the text to the desired language
    translated_text = translator.translate(sentence, src=source_language, dest=destination_language)

    st.write(f"Source Language: {source_language_name}")
    st.write(f"Sentence: {sentence}")
    st.write(f"Destination Language: {destination_language_name}")
    st.write(f"Translated Text: {translated_text.text}")

    # Using Google-Text-to-Speech to speak the translated text
    speak = gTTS(text=translated_text.text, lang=destination_language, slow=False)
    speak.save("translated_voice.mp3")

    # Play the translated voice
    playsound('translated_voice.mp3')

if st.button("  CLICK HERE TO TRANSLATE  "):
    translate_speech()





