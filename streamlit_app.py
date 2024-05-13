import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

st.title('Recherche de Médias')




import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


api_key = 'AIzaSyBHktH6XIGar0v7UStL1reXQUyx8aqxHwg'
api_service_name = 'youtube'
api_version = 'v3'

st.title('Recherche de Médias')

# Créer une barre de recherche
query = st.text_input("Entrez votre recherche:", "")

if query:
    st.write(f"Vous avez recherché: {query}")

# Construire le service YouTube
try:
    youtube = build(api_service_name, api_version, developerKey=api_key)

    # Effectuer la requête à l'API YouTube
    request = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=10,
        order='relevance',
        safeSearch = 'moderate',
        type='video',
        relevanceLanguage='fr'
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

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(video_thumbnail)
            with col2:
                st.write(video_title)
                if st.button('Voir transcription', key=video_id):
                    display_transcription(video_id)

    else:
        st.write("Aucun résultat trouvé.")

except HttpError as e:
    st.error("Une erreur s'est produite lors de l'appel à l'API YouTube.")
    st.error(e)


try:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript(['fr'])

    st.subheader("Transcription de la vidéo")
    transcript_data = transcript.fetch()
    for text_segment in transcript_data:
        st.write(f"{text_segment['text']}")

except (TranscriptsDisabled, NoTranscriptFound):
    st.write("La transcription n'est pas disponible pour cette vidéo.")
except Exception as e:
    st.write("Une erreur s'est produite lors de la récupération de la transcription.")
    st.write(str(e))


