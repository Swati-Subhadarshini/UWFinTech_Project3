import streamlit as st
from pathlib import Path
import pandas as pd

# Import upcoming_games.csv
upcoming_games = pd.read_csv(Path("Resources/upcoming_games.csv"))
upcoming_games = upcoming_games.drop(columns="Unnamed: 0")

# Create games in CSV as individual variables.
Team_1 = f"{upcoming_games.iloc[0,2]} : {upcoming_games.iloc[0,3]}"
Team_2 = f"{upcoming_games.iloc[0,4]} : {upcoming_games.iloc[0,5]}"

# Here begins the Streamlit Interface code.
st.markdown('# SuperBowl Bet Machine')
st.markdown('## Teams & Odds')
st.dataframe(upcoming_games)

st.markdown('### Place your bets here!')
st.text_input('Enter your public address')
st.selectbox('Choose YOUR winner:', [Team_1, Team_2])
st.number_input('Wager Amount')

if st.button('Place Bet'):
    st.write("A bunch of crazy stuff just happened in the background and your bet is on blockchain")
