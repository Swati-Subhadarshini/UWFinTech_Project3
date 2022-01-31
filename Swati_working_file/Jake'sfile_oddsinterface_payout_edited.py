# Library & Module Imports
from ast import Delete
import streamlit as st
from pathlib import Path
import pandas as pd
#import os
#import json
#from dotenv import load_dotenv
#from web3 import Web3
#import odds_request
#import get_winners

####################
# Web 3 Connection
###################
# Define and connect a new Web3 provider
#w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Cache the contract on load
#@st.cache(allow_output_mutation=True)
# Define the load_contract function
#def load_contract():

    # Load Art Gallery ABI
    #with open(Path('bet_slip_abi.json')) as f:
        #bet_slip_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    #contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    #contract = w3.eth.contract(
        #address=contract_address,
        #abi=bet_slip_abi
    #)
    # Return the contract from the function
    #return contract

# Load the contract
#contract = load_contract()

######################################
# Python Code & Python Module Imports
######################################


# Import upcoming_games.csv
upcoming_games = pd.read_csv(Path("Resources/upcoming_games.csv"))
upcoming_games = upcoming_games.drop(columns="Unnamed: 0")

# Create games in CSV as individual variables.
# Could potentially create some sort of function for-loop that checks how many rows are in the upcoming_games.csv
# and returns that many Team variables.
Team_0 = " "
Team_1 = f"{upcoming_games.iloc[0,2]} : {upcoming_games.iloc[0,3]}"
Team_2 = f"{upcoming_games.iloc[0,4]} : {upcoming_games.iloc[0,5]}"
Team_3 = f"{upcoming_games.iloc[1,2]} : {upcoming_games.iloc[1,3]}"
Team_4 = f"{upcoming_games.iloc[1,4]} : {upcoming_games.iloc[1,5]}"

###########################
# Streamlit Interface code.
###########################

# Cover Image & Titles
st.image("Resources/Footballfield.jpeg")
st.markdown('# SuperBowl Bet Machine')
st.markdown('## Current Week Matchups & Odds')

# Button to refresh games dataframe. Costs an API Call.
if st.button("If games are not current, click here and then refresh the page."):
    odds_request.update_games()

# Show current week betting options
st.dataframe(upcoming_games)

# Create form for submitting bet widgets

with st.form(key='place_bet'):
    st.markdown('### Place your bets here!')
    user_address = st.text_input('Enter your public address')
    user_name = st.text_input('Enter your UserName')
    user_bet_selection = st.selectbox('Choose YOUR winner:', [Team_0,  Team_1, Team_2, Team_3, Team_4])
    user_wager = st.number_input('Wager Amount', min_value=0)
    # earned_payout will be 0 unless the bet wins and then it will equal potential_payout
    #earned_payout = st.text('Earned Payout Placeholder')
    submitted = submit_button = st.form_submit_button(label='Submit Bet')

    # Potential payout: Need to find a good way to take the odds from the bet selection and do the math to calculate the payout.
    # Probably an if statement. 
    #potential_payout = profit_earned + user_wager
    if submitted:
        st.write('Your selected Team:', user_bet_selection)
        odds = user_bet_selection.split(':')
        odd_value = int(odds[1])        
        if odd_value > 0:
            earned_amount = (odd_value / 100) * user_wager
        else:
            odd_value = odd_value * (-1)
            earned_amount = (100 / odd_value) * user_wager
        st.write('Odd value is:', odd_value)
        st.write('Earned Payout:', earned_amount)    
        st.write('Potential Payout:', earned_amount + user_wager)


  
    
    
   
 
   
     

    
