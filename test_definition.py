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

# Streamlit app
st.title("English Word Definition Finder")

word = st.text_input("Enter a word:")

if word:
    definition = dictionary.meaning(word)
    if definition:
        st.write(f"**Definition of {word}:**")
        for pos, defs in definition.items():
            st.write(f"**{pos}:**")
            for d in defs:
                st.write(f"- {d}")
    else:
        st.write("No definition found.")
else:
    st.write("Please enter a word to get its definition.")
