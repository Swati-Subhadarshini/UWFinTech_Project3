# Library & Module Imports
import streamlit as st
from pathlib import Path
import pandas as pd
import os
import json
from dotenv import load_dotenv
from web3 import Web3
import odds_request
import get_winners


####################
# Web 3 Connection
###################
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('bet_slip_abi.json')) as f:
        bet_slip_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=bet_slip_abi
    )
    # Return the contract from the function
    return contract

# Load the contract
contract = load_contract()

######################################
# Python Code & Python Module Imports
######################################

# Import upcoming_games.csv
upcoming_games = pd.read_csv(Path("Resources/upcoming_games.csv"))
upcoming_games = upcoming_games.drop(columns="Unnamed: 0")

# Create games in CSV as individual variables.
# Could potentially create some sort of function for-loop that checks how many rows are in the upcoming_games.csv
# and returns that many Team variables.
Team_1 = f"{upcoming_games.iloc[0,2]} : {upcoming_games.iloc[0,3]}"
Team_2 = f"{upcoming_games.iloc[0,4]} : {upcoming_games.iloc[0,5]}"
Team_3 = f"{upcoming_games.iloc[1,2]} : {upcoming_games.iloc[1,3]}"
Team_4 = f"{upcoming_games.iloc[1,4]} : {upcoming_games.iloc[1,5]}"

# Create Submitted bet dataframe in session_state. This dataframe will persist through sessions until the cache is cleared.
#if "df" not in st.session_state:
#    st.session_state.df = pd.DataFrame(columns=['user_name', 'bet_selection', 'wager_amount', 'earned_payout', 'bet_status'])
st.session_state.df = pd.DataFrame(columns=['user_name', 'bet_selection', 'wager_amount', 'earned_payout', 'bet_status'])


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
    user_bet_selection = st.selectbox('Choose YOUR winner:', [Team_1, Team_2, Team_3, Team_4])
    user_wager = st.number_input('Wager Amount', min_value=0)
    # Potential payout: Need to find a good way to take the odds from the bet selection and do the math to calculate the payout.
    # Probably an if statement. 
        # If odds are positive:
        # odds / 100 * wager = Potential payout
        # If odds are negative:
        # 100 / odds * wager = Potential payout
    potential_payout = st.text('Potential Payout Placeholder')
    # earned_payout will be 0 unless the bet wins and then it will equal potential_payout
    earned_payout = st.text('Earned Payout Placeholder')
    submitted = submit_button = st.form_submit_button(label='Submit Bet')
    if submitted:
        # Send to smart contract.
        try:
            contract.functions.placeBet(user_address, user_name, user_bet_selection).transact({'from': user_address, 'value': w3.toWei(user_wager,'wei'), 'gas': 1000000})
            # Add inputs to dataframe.
            betID = (contract.functions.totalSupply().call()-1)
            st.write(f"Your betID is: {betID}")
            if(betID <= 9):
                for n in range(0, betID+1):
                    user_name, user_bet_selection, user_wager, earned_payout, bet_status = contract.functions.reviewBet(n).call()
                    new_row = {'user_name':user_name, 'bet_selection':user_bet_selection, 'wager_amount':user_wager, 'earned_payout':earned_payout, 'bet_status':bet_status}
                    st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
            else:
                for n in range(betID-9, betID+1):
                    user_name, user_bet_selection, user_wager, earned_payout, bet_status = contract.functions.reviewBet(n).call()
                    new_row = {'user_name':user_name, 'bet_selection':user_bet_selection, 'wager_amount':user_wager, 'earned_payout':earned_payout, 'bet_status':bet_status}
                    st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
        except:
            st.write("Your bet is too large.")

# Submitted bets dataframe
st.dataframe(st.session_state.df)


# Display bet function.
st.sidebar.markdown('## Display Bet')
with st.sidebar.form(key="check_bet"):
    betID = st.number_input("Enter a Bet Token ID to display", value=0, step=1)
    submitted = submit_button = st.form_submit_button(label='Display Bet')
    if submitted:
        user_name, user_bet_selection, user_wager, earned_payout, bet_status = contract.functions.reviewBet(betID).call()
        st.write(f"Username:{user_name}")
        st.write(f"Selected Bet:{user_bet_selection}")
        st.write(f"Wager:{user_wager} Wei")
        #st.write(f"Potential Payout:{potential_payout} Wei") #Add this in final streamlit app
        st.write(f"Earned Payout:{earned_payout} Wei")
        st.write(f"Bet Status:{bet_status}")

# Payout bet form & function
st.sidebar.markdown('## Cash-In Winning Bet')
with st.sidebar.form(key="cash_bet"):
    winner_betID = st.number_input("Enter a Bet Token ID to Cash-In Winning Bet:", step=1)
    winner_user_address = st.text_input('Enter your public address used to place bet:')
    submitted = submit_button = st.form_submit_button(label='Cash Winning Bet')
    if submitted:
        try:
            contract.functions.winnerCashout(winner_betID, winner_user_address).transact({'from': user_address, 'gas': 1000000})
        except:
            st.write("No access to this bet or you did not win.")

st.image("Resources/weeklyresultsbanner.png")

###############################
# Get Weekly Results Function
###############################
season_year = [2020, 2021, 2022]
season_week = list(range(0,24))
with st.form(key = "Weekly_Results"):
    st.markdown("### Check Week Winners Here")
    year = st.selectbox("Select Year", season_year)
    week = st.selectbox("Select Week", season_week)
    submitted = submit_button = st.form_submit_button(label='Get Weekly Results')
    if submitted:
        week_schedule = get_winners.get_week_schedule(week, year)
        st.dataframe(week_schedule)
