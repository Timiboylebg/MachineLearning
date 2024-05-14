import streamlit as st
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Configuration API
api_key = 'YOUR_YOUTUBE_API_KEY'
news_api_key = 'YOUR_NEWSAPI_KEY'
api_service_name = 'youtube'
api_version = 'v3'

# Titre de l'application
st.title('Search for media that interests you')

# Sélection de la page
page = st.sidebar.selectbox("Choose a page:", ["Videos", "News"])

# Créer une barre de recherche
query = st.text_input("Enter your search:", "")
language = st.selectbox("Choose video language:", ["en", "fr"])  # Sélecteur de langue

if query:
    st.write(f"You searched for: {query}")

if page == "Videos":
    # Section pour les vidéos
    try:
        youtube = build(api_service_name, api_version, developerKey=api_key)
        request = youtube.search().list(
            part='snippet',
            q=query,
            maxResults=4,
            order='relevance',
            safeSearch='moderate',
            type='video',
            relevanceLanguage=language,
            channelId='UCAuUUnT6oDeKwE6v1NGQxug'
        )
        response = request.execute()

        for item in response.get('items', []):
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_thumbnail = item['snippet']['thumbnails']['high']['url']

            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.image(video_thumbnail)
            with col2:
                st.write(video_title)
            with col3:
                if st.button("Show Transcript", key=video_id):
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        for text in transcript:
                            st.write(text['text'])
                    except TranscriptsDisabled:
                        st.error("Transcripts are disabled for this video.")
                    except NoTranscriptFound:
                        st.error("No transcript found for this video.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

    except HttpError as e:
        st.error("An error occurred with the YouTube API.")
        st.error(e)

elif page == "News":
    # Section pour les articles de presse
    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={news_api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            articles_data = response.json()

            if articles_data['status'] == 'ok' and articles_data['totalResults'] > 0:
                for article in articles_data['articles']:
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
