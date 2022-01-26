import streamlit as st
from pathlib import Path
import pandas as pd

#Jake's Work/Python_Modules/Resources/upcoming_games.csv
# Import upcoming_games.csv
upcoming_games = pd.read_csv(Path("../Python_Modules/Resources/upcoming_games.csv"))
upcoming_games = upcoming_games.drop(columns="Unnamed: 0")

# Create games in CSV as individual variables.
Team_1 = f"{upcoming_games.iloc[0,2]} : {upcoming_games.iloc[0,3]}"
Team_2 = f"{upcoming_games.iloc[0,4]} : {upcoming_games.iloc[0,5]}"
Team_3 = f"{upcoming_games.iloc[1,2]} : {upcoming_games.iloc[1,3]}"
Team_4 = f"{upcoming_games.iloc[1,4]} : {upcoming_games.iloc[1,5]}"

# Here begins the Streamlit Interface code.

# Cover Image & Titles
st.image("./Footballfield.jpeg")
st.markdown('# SuperBowl Bet Machine')
st.markdown('## Current Week Matchups & Odds')

# Show current week betting options
st.dataframe(upcoming_games)

# Create form for submitting bet widgets
with st.form(key='place_bet'):
    st.markdown('### Place your bets here!')
    user_address = st.text_input('Enter your public address')
    user_name = st.text_input('Enter your UserName')
    user_bet_selection = st.selectbox('Choose YOUR winner:', [Team_1, Team_2, Team_3, Team_4])
    user_wager = st.number_input('Wager Amount')
    potential_payout = st.text('Potential Payout Placeholder')
    earned_payout = st.text('Earned Payout Placeholder')
    submitted = submit_button = st.form_submit_button(label='Submit Bet')
    if submitted:
        st.write(
            str(user_address),
            str(user_name),
            str(user_bet_selection),
            int(user_wager),
            # int(potential_payout),
            # int(earned_payout)
        )
        st.write("BetID")

# Call block function. Checks to see if bet has finished.
st.markdown('## Check Bet Status')
with st.form(key="check_bet"):
    user_betID = st.text_input('Input your BetID')
    submitted = submit_button = st.form_submit_button(label='Check Bet Status')
    if submitted:
        st.write('Run check bet function')

