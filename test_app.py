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


language = st.selectbox("Choose video language:", ["en", "fr"])  # Sélecteur de langue

if query:
    st.write(f"Vous avez recherché: {query}")


# Section de recherche pour YouTube dans la première colonne


youtube = build(api_service_name, api_version, developerKey=api_key)

request = youtube.search().list(
    part='snippet',
    q='changement climatique',
    maxResults=1,
    order='relevance',
    safeSearch='moderate',
    type='video',
    relevanceLanguage=language
)
response = request.execute()

for item in response.get('items', []):
    video_id = item['id']['videoId']
    print(f"Video ID: {video_id}")


st.button("Show Transcript", key=video_id):  # Key must be unique for each button
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




