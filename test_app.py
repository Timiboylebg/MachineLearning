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
    
    # Champ de saisie pour le mot en anglais
    word = st.text_input("Entrez un mot en anglais:")
    
    if word:
        # Appeler la fonction de traduction
        translation = translate_word(word)
        
        # Afficher la traduction
        st.write(f"Traduction en français: {translation}")

if __name__ == "__main__":
    main()
