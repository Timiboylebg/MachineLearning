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
    formatted_text = " ".join([f'<a href="javascript:void(0)" onclick="sendWord(\'{word}\')">{word}</a>' for word in words])
    st.markdown(formatted_text, unsafe_allow_html=True)

    # Ajouter un script JavaScript pour envoyer le mot cliqué à Streamlit
    st.markdown("""
        <script>
        function sendWord(word) {
            const streamlitApi = window.parent.Streamlit;
            streamlitApi.setComponentValue(word);
        }
        </script>
    """, unsafe_allow_html=True)

    # Afficher la liste de vocabulaire
    if st.session_state.vocab_list:
        st.write("Votre liste de vocabulaire:")
        for vocab_word in st.session_state.vocab_list:
            translation = translate_word(vocab_word)
            st.write(f"{vocab_word} - {translation}")

    # Configurer le composant Streamlit pour recevoir le mot cliqué
    st.components.v1.html("""
        <div id="streamlit-mount"></div>
        <script>
        const streamlitMount = document.getElementById('streamlit-mount');
        const handleStreamlitMessage = (event) => {
            if (event.data.type === 'streamlit:setComponentValue') {
                streamlitMount.dispatchEvent(new CustomEvent('streamlit:value', { detail: event.data.value }));
            }
        };
        window.addEventListener('message', handleStreamlitMessage);
        </script>
    """)
    
    # Recevoir le mot cliqué et l'ajouter à la liste de vocabulaire
    if st.session_state.get('last_word') != st.session_state.get('streamlit_value'):
        st.session_state['last_word'] = st.session_state.get('streamlit_value')
        if st.session_state['last_word'] and st.session_state['last_word'] not in st.session_state.vocab_list:
            st.session_state.vocab_list.append(st.session_state['last_word'])

if __name__ == "__main__":
    main()
