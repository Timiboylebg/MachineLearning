import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        order='date',
        type='video'
    )
    response = request.execute()

    # Afficher les résultats
    if response.get('items', []):
        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            # Afficher le titre avec un lien vers la vidéo
            st.markdown(f"[{video_title}]({video_url})")

    else:
        st.write("Aucun résultat trouvé.")

except HttpError as e:
    st.error("Une erreur s'est produite lors de l'appel à l'API YouTube.")
    st.error(e)


url = 'https://raw.githubusercontent.com/michalis0/MGT-502-Data-Science-and-Machine-Learning/main/data/yield_df.csv'
df_yield= pd.read_csv(url)

# Assuming df_yield is your DataFrame
data = df_yield['Item'].value_counts().reset_index()
data.columns = ['Item', 'count']  # Rename columns for clarity


# Create a pie chart using Plotly Express
fig = px.pie(data, names='Item', values='count', title='Shares of crops')

# Display the pie chart using Streamlit
st.plotly_chart(fig)
