import streamlit as st
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator

def main():
    st.title("Traducteur Anglais -> Français")
    
    # Créer une instance de Translator
    translator = Translator()
    
    # Champ de saisie pour le mot en anglais
    word = st.text_input("Entrez un mot en anglais:")
    
    if word:
        # Traduire le mot
        translation = translator.translate(word, src='en', dest='fr')
        
        # Afficher la traduction
        st.write(f"Traduction en français: {translation.text}")

if __name__ == "__main__":
    main()


