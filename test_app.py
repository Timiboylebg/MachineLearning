import streamlit as st
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator


st.title("Traducteur Francais -> Anglais")

# Créer une instance de Translator
translator = Translator()

# Champ de saisie pour le mot en anglais
word = st.text_input("Entrez un mot en francais:")

if word:
    # Traduire le mot
    translation = translator.translate(word, src='fr', dest='en')
    
    # Afficher la traduction
    st.write(f"Traduction en anglais: {translation.text}")

def translate_word(word):
    """
    Fonction pour traduire un mot de l'anglais vers le français.
    
    Args:
    word (str): Le mot en anglais à traduire.
    
    Returns:
    str: La traduction en français du mot.
    """
    translator = Translator()
    translation = translator.translate(word, src='en', dest='fr')
    return translation.text

 # Champ de saisie pour le mot en anglais
word = st.text_input("Entrez un mot en anglais:")

if word:
    # Appeler la fonction de traduction
    translation = translate_word(word)
    
    # Afficher la traduction
    st.write(f"Traduction en français: {translation}")

# Exemple de texte en anglais
text = "This is an example text where each word can be clicked to add to your vocabulary list."

# Liste pour stocker le vocabulaire sélectionné
if 'vocab_list' not in st.session_state:
    st.session_state.vocab_list = []

# Afficher le texte et permettre de cliquer sur chaque mot
st.write("Cliquez sur un mot pour l'ajouter à votre liste de vocabulaire:")
words = text.split()
for idx, word in enumerate(words):
    if st.button(word, key=idx):
        st.session_state.vocab_list.append(word)

# Afficher la liste de vocabulaire
if st.session_state.vocab_list:
    st.write("Votre liste de vocabulaire:")
    for vocab_word in st.session_state.vocab_list:
        translation = translate_word(vocab_word)
        st.write(f"{vocab_word} - {translation}")



