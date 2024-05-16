import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import requests
from google.cloud import translate_v2 as translate


api_key = 'AIzaSyBHktH6XIGar0v7UStL1reXQUyx8aqxHwg'
news_api_key = '00bd707fafb54308842886874d3b23a5'
api_service_name = 'youtube'
api_version = 'v3'

if 'vocab_list' not in st.session_state:
    st.session_state.vocab_list = []

        
# Fonction pour évaluer le niveau de langue
def evaluate_language_level(text):
    words = text.split()
    num_words = len(words)
    if num_words < 50:
        return "A1"
    elif num_words < 100:
        return "A2"
    elif num_words < 150:
        return "B1"
    elif num_words < 200:
        return "B2"
    elif num_words < 250:
        return "C1"
    else:
        return "C2"

st.sidebar.image("logo.png", width=200)

st.title('Search for a media that interest you')

# Sélection de la page
page = st.sidebar.selectbox("Choose a page:", ["Videos", "News","Vocabulary List"])

# Créer une barre de recherche
query = st.text_input("Entrez votre recherche:", "")

language = st.selectbox("Choose video language:", ["en", "fr"])  # Sélecteur de langue

if query:
    st.write(f"Vous avez recherché: {query}")


# Section de recherche pour YouTube 
if page == "Videos":
# Construire le service YouTube
    try:
        youtube = build(api_service_name, api_version, developerKey=api_key)
    
        # Effectuer la requête à l'API YouTube
        request = youtube.search().list(
            part='snippet',
            q=query,
            maxResults=4,
            order='relevance',
            safeSearch = 'moderate',
            type='video',
            relevanceLanguage= language,
            channelId='UCAuUUnT6oDeKwE6v1NGQxug' 
        )
        response = request.execute()
    
        # Afficher les résultats
        if response.get('items', []):
            for item in response['items']:
                video_title = item['snippet']['title']
                video_id = item['id']['videoId']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                video_thumbnail = item['snippet']['thumbnails']['high']['url']
                video_description = item['snippet']['description']
    
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.image(video_thumbnail)
                with col2:
                    st.write(video_title)
                with col3:
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        full_text = " ".join([text['text'] for text in transcript])
                        level = evaluate_language_level(full_text)
                        st.write("Language Level:", level)
                        st.button(f"Level: {level}", key=level)
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

                # Bouton pour afficher le transcript
                if st.button("Show Transcript", key=f"btn_{video_id}"):  # Clé unique pour chaque bouton
                    try:
                        # Récupération du transcript de la vidéo
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        # Affichage du transcript
                        for text in transcript:
                            st.write(text['text'])
                    except TranscriptsDisabled:
                        st.error("Transcripts are disabled for this video.")
                    except NoTranscriptFound:
                        st.error("No transcript found for this video.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                st.markdown("---")
        else:
            st.write("Aucun résultat trouvé.")
    
    except HttpError as e:
        st.error("Une erreur s'est produite lors de l'appel à l'API YouTube.")
        st.error(e)

if page == "News":
    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={news_api_key}&pageSize=5'
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles_data = response.json()

            if articles_data['status'] == 'ok' and articles_data['totalResults'] > 0:
                for article in articles_data['articles']:
                    title = article['title']
                    description = article['description'] or "No description available"  # Fallback for empty description
                    url = article['url']

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(title)
                        st.write(description)
                        st.write(f"[Read more]({url})")

                                
                    with col2:
                        # Évaluer et afficher le niveau de langue
                        level = evaluate_language_level(description)
                        st.button(f"Level: {level}", key=title)  # Use title as unique key for button
                    st.markdown("---")
            else:
                st.write("No articles found.")

        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


vocab_list = ["bonjour", "maison", "ordinateur", "chat", "chien"]


if page == "Vocabulary List":
    st.header("Vocabulary List")
    





# Vérifier si un mot a été ajouté via la requête HTTP
if 'word' in st.experimental_get_query_params():
    word_to_add = st.experimental_get_query_params()['word'][0]
    add_word(word_to_add)
