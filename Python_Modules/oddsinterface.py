import streamlit as st
from pathlib import Path
import pandas as pd


upcoming_games = pd.read_csv(Path("Resources/upcoming_games.csv"))
upcoming_games = upcoming_games.drop(columns="Unnamed: 0")

Team_1 = f"{upcoming_games.iloc[0,2]} : {upcoming_games.iloc[0,3]}"
Team_2 = f"{upcoming_games.iloc[0,4]} : {upcoming_games.iloc[0,5]}"

st.markdown('# Streamlit Test for Displaying Odds')
st.markdown('## This weeks matchups and odds!')
st.dataframe(upcoming_games)

st.markdown('### Place your bets here!')
st.selectbox('Choose YOUR winner:', [Team_1, Team_2])
st.number_input('Wager Amount')
if st.button('Place Bet'):
    st.write("A bunch of crazy stuff just happened in the background and your bet is on blockchain")





