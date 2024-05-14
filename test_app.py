import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import requests


api_key = 'AIzaSyBHktH6XIGar0v7UStL1reXQUyx8aqxHwg'
news_api_key = '00bd707fafb54308842886874d3b23a5'
api_service_name = 'youtube'
api_version = 'v3'

st.title('Search for a media that interest you')


# Créer une barre de recherche
query = st.text_input("Entrez votre recherche:", "")

language = st.selectbox("Choose video language:", ["en", "fr"])  # Sélecteur de langue

if query:
    st.write(f"Vous avez recherché: {query}")


# Section de recherche pour YouTube dans la première colonne

try:
    youtube = build(api_service_name, api_version, developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=4,
        order='relevance',
        safeSearch='moderate',
        type='video',
        relevanceLanguage=language
    )
    response = request.execute()

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
                st.write(video_description)
                st.write(f'[Watch Video]({video_url})')
            with col3:
                if st.button("Show Transcript", key=video_id):  # Key must be unique for each button
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        for text in transcript:
                            st.write(text['text'])
                    except TranscriptsDisabled:
                        st.error("Transcript is disabled for this video.")
                    except NoTranscriptFound:
                        st.error("No transcript found for this video.")
    else:
        st.write("No results found.")

except HttpError as e:
    st.error("An error occurred with the YouTube API.")
    st.error(e)


