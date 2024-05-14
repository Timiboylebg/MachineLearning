import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import requests



st.title('Search for a media that interest you')



# Key must be unique for each button

transcript = YouTubeTranscriptApi.get_transcript('fxbCHn6gE3U')
for text in transcript:
    st.write(text['text'])




