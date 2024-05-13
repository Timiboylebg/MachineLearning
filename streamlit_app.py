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
        relevanceLanguage= language
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
                

    else:
        st.write("Aucun résultat trouvé.")

except HttpError as e:
    st.error("Une erreur s'est produite lors de l'appel à l'API YouTube.")
    st.error(e)


st.header("News Article Search")
query_news = st.text_input("Enter your NewsAPI search:", "")

if query_news:
    st.write(f"You searched for articles about: {query_news}")
    url = f'https://newsapi.org/v2/everything?q={query_news}&language={language}&apiKey={news_api_key}'

    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Cela lèvera une exception pour les codes de statut 4XX ou 5XX
        articles_data = response.json()  # Convertit la réponse en JSON

        if articles_data['status'] == 'ok' and articles_data['totalResults'] > 0:
            articles = articles_data['articles']
            for article in articles:
                st.subheader(article['title'])
                st.write(article['description'])
                st.write(f"Read more: {article['url']}")
        else:
            st.write("No articles found.")
            
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")







