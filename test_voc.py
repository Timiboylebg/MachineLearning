import streamlit as st
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator
from PyDictionary import PyDictionary

# Initialize Translator and PyDictionary
translator = Translator()
dictionary = PyDictionary()

# Function to translate text from French to English
def translate_to_english(word):
    translation = translator.translate(word, src='fr', dest='en')
    return translation.text

# Function to get a single definition of a word
def get_single_definition(word):
    meaning = dictionary.meaning(word)
    if meaning:
        for pos, defs in meaning.items():
            if defs:
                return defs[0]
    return "No definition found."

# Sample French text
sample_text = """
Le monde moderne est rempli de technologies avancées qui facilitent la vie quotidienne. 
Les ordinateurs, les smartphones et l'internet sont devenus indispensables pour travailler, 
communiquer et se divertir. Cependant, il est important de se rappeler de prendre des pauses 
et de profiter de la nature et de la compagnie de nos proches.
"""

# Navigation menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["French Text & Vocabulary Input", "Vocabulary List & Definitions"])

if page == "French Text & Vocabulary Input":
    st.title("French Text & Vocabulary Input")
    
    st.subheader("Text in French")
    st.write(sample_text)
    
    st.subheader("Enter words you don't understand (separated by commas):")
    vocab_input = st.text_area("Vocabulary List", "ex: technologies, indispensables, compagnie")
    
    if st.button("Save Vocabulary List"):
        vocab_list = [word.strip() for word in vocab_input.split(',')]
        st.session_state['vocab_list'] = vocab_list
        st.success("Vocabulary list saved!")

elif page == "Vocabulary List & Definitions":
    st.title("Vocabulary List & Definitions")
    
    if 'vocab_list' in st.session_state:
        vocab_list = st.session_state['vocab_list']
        
        st.subheader("Vocabulary Table")
        
        vocab_data = []
        
        for word in vocab_list:
            translation = translate_to_english(word)
            definition = get_single_definition(translation)
            vocab_data.append({"French Word": word, "English Translation": translation, "English Definition": definition})
        
        st.table(vocab_data)
    else:
        st.warning("No vocabulary list found. Please go to the 'French Text & Vocabulary Input' page and enter some words.")
