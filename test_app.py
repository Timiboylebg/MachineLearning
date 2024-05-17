import streamlit as st
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator

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

def main():
    st.title("Traducteur Anglais -> Français")
    
    # Exemple de texte en anglais
    text = "This is an example text where each word can be clicked to add to your vocabulary list."
    
    # Liste pour stocker le vocabulaire sélectionné
    if 'vocab_list' not in st.session_state:
        st.session_state.vocab_list = []

    # Afficher le texte et permettre de cliquer sur chaque mot
    st.write("Cliquez sur un mot pour l'ajouter à votre liste de vocabulaire:")

    # Utiliser des liens HTML pour chaque mot
    words = text.split()
    for word in words:
        if st.button(word):
            st.session_state.vocab_list.append(word)
    
    # Afficher la liste de vocabulaire
    if st.session_state.vocab_list:
        st.write("Votre liste de vocabulaire:")
        for vocab_word in st.session_state.vocab_list:
            translation = translate_word(vocab_word)
            st.write(f"{vocab_word} - {translation}")

if __name__ == "__main__":
    main()
    main()
