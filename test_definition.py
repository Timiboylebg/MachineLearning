import streamlit as st
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator
from PyDictionary import PyDictionary


# Initialize PyDictionary
dictionary = PyDictionary()
# Initialize Translator
translator = Translator()

# Function to get a single definition of a word
def get_single_definition(word):
    meaning = dictionary.meaning(word)
    if meaning:
        # Choose the first definition from the first part of speech
        for pos, defs in meaning.items():
            if defs:
                return defs[0]
    return None

# Function to translate text from English to French
def translate_to_french(word):
    translation = translator.translate(word, src='en', dest='fr')
    return translation.text

# Function to translate text from French to English
def translate_to_english(word):
    translation = translator.translate(word, src='fr', dest='en')
    return translation.text

# Streamlit app
st.title("Word Definition Finder")

st.header("English to French Definition")
word_en = st.text_input("Enter a word in English:")

if word_en:
    definition = get_single_definition(word_en)
    if definition:
        translation_fr = translate_to_french(definition)
        st.write(f"**Definition of {word_en} in French:**")
        st.write(f"{word_en} = {translation_fr}")
    else:
        st.write("No definition found.")
else:
    st.write("Please enter a word to get its definition.")

st.header("French to English Definition")
word_fr = st.text_input("Enter a word in French:")

if word_fr:
    translation_en = translate_to_english(word_fr)
    if translation_en:
        definition_en = get_single_definition(translation_en)
        if definition_en:
            st.write(f"**Definition of {word_fr} (translated to {translation_en}) in English:**")
            st.write(f"{translation_en} = {definition_en}")
        else:
            st.write("No definition found for the translated word.")
    else:
        st.write("Translation failed.")
else:
    st.write("Please enter a word to get its definition.")
