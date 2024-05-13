import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Recherche de Médias')

# Créer une barre de recherche
query = st.text_input("Entrez votre recherche:", "")

# Vous pouvez afficher la requête entrée par l'utilisateur pour confirmation
if query:
    st.write(f"Vous avez recherché: {query}")

url = 'https://raw.githubusercontent.com/michalis0/MGT-502-Data-Science-and-Machine-Learning/main/data/yield_df.csv'
df_yield= pd.read_csv(url)

# Assuming df_yield is your DataFrame
data = df_yield['Item'].value_counts().reset_index()
data.columns = ['Item', 'count']  # Rename columns for clarity


# Create a pie chart using Plotly Express
fig = px.pie(data, names='Item', values='count', title='Shares of crops')

# Display the pie chart using Streamlit
st.plotly_chart(fig)
