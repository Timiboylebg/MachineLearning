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
translator = Translator(to_lang="fr")

# Function to get a single definition of a word
def get_single_definition(word):
    meaning = dictionary.meaning(word)
    if meaning:
        # Choose the first definition from the first part of speech
        for pos, defs in meaning.items():
            if defs:
                return defs[0]
    return None

# Streamlit app
st.title("French Word Definition Finder")

word = st.text_input("Enter a word in English:")

if word:
    definition = get_single_definition(word)
    if definition:
        translation = translator.translate(definition)
        st.write(f"**Definition of {word} in French:**")
        st.write(translation)
    else:
        st.write("No definition found.")
else:
    st.write("Please enter a word to get its definition.")
