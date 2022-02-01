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
    with open(Path('./contracts/compiled/bet_slip_abi.json')) as f:
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
# Team_3 = f"{upcoming_games.iloc[1,2]} : {upcoming_games.iloc[1,3]}"
# Team_4 = f"{upcoming_games.iloc[1,4]} : {upcoming_games.iloc[1,5]}"

# Create Submitted bet dataframe in session_state. This dataframe will persist through sessions until the cache is cleared.
#if "df" not in st.session_state:
#    st.session_state.df = pd.DataFrame(columns=['user_name', 'bet_selection', 'wager_amount', 'earned_payout', 'bet_status'])
st.session_state.df = pd.DataFrame(columns=['user_name', 'bet_selection', 'wager_amount', 'earned_payout', 'bet_status'])

# List of acceptable bet status
status_list = ["Pending", "Loser", "Winner", "Complete"]


###########################
# Streamlit Interface code.
###########################

# Cover Image & Titles
st.image("Resources/Footballfield.jpeg")
st.markdown('# SuperBowl Bet Machine')
st.markdown('## Current Week Matchups & Odds')

###########################
# User Functions
###########################

# Button to refresh games dataframe. Costs an API Call.
if st.button("Refresh Current Week Matchups (Costs an API Call)"):
    odds_request.update_games()

# Show current week betting options
st.dataframe(upcoming_games)


# Create form for submitting bet widgets
with st.form(key='place_bet'):
    st.markdown('### Place your bets here!')
    user_address = st.text_input('Enter your public address')
    user_name = st.text_input('Enter your UserName')
    user_bet_selection = st.selectbox('Choose YOUR winner:', [Team_1, Team_2])
    user_wager = st.number_input('Wager Amount (In WEI)', min_value=0, value=0, step=1)
    # Potential payout: Need to find a good way to take the odds from the bet selection and do the math to calculate the payout.
    # Probably an if statement. 
        # If odds are positive:
        # odds / 100 * wager = Potential payout
        # If odds are negative:
        # 100 / odds * wager = Potential payout
    submitted = submit_button = st.form_submit_button(label='Submit Bet')
    if submitted:
        # Send to smart contract.
        try:
            contract.functions.placeBet(user_address, user_name, user_bet_selection).transact({'from': user_address, 'value': w3.toWei(user_wager,'wei'), 'gas': 1000000})
            # Add inputs to dataframe.
            betID = (contract.functions.totalSupply().call()-1)
            st.write(f"Your betID is: {betID}")

            # Calculating Potential Winnigs & Total Payout
            st.write('Your Selection:', user_bet_selection)
            odds = user_bet_selection.split(':')
            odd_value = int(odds[1])        
            if odd_value > 0:
                earned_amount = (odd_value / 100) * user_wager
            else:
                odd_value = odd_value * (-1)
                earned_amount = (100 / odd_value) * user_wager
            st.write('Odds value is:', odd_value)
            st.write('Potential Winnings:', earned_amount)    
            st.write('Total Payout:', earned_amount + user_wager)
            
        except:
            st.write("Incomplete user data or your bet is too large.")
        
        

# Create form for viewing the latest 10 bets
with st.form(key='view_latest_bets'):
    st.markdown('### Update to view the latest 10 bets here!')
    submitted = submit_button = st.form_submit_button(label='View Latest')
    if submitted:
        # Pull the latest 10 bets from the blockchain ledger to view.
        try:
            betID = (contract.functions.totalSupply().call()-1)
            # If betID is less than 9, view all bets in a dataframe.
            if(betID <= 9):
                sub_index = range(0, betID+1)
                for n in sub_index:
                    user_name, user_bet_selection, user_wager, earned_payout, bet_status = contract.functions.reviewBet(n).call()
                    new_row = {'user_name':user_name, 'bet_selection':user_bet_selection, 'wager_amount':user_wager, 'earned_payout':earned_payout, 'bet_status':bet_status}
                    st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
                    #st.session_state.df.set_index(range(0,betID+1))
            # If betID is greater than 9, view latest 10 bets in a dataframe.
            else:
                sub_index = range(betID-9, betID+1)
                for n in sub_index:
                    user_name, user_bet_selection, user_wager, earned_payout, bet_status = contract.functions.reviewBet(n).call()
                    new_row = {'user_name':user_name, 'bet_selection':user_bet_selection, 'wager_amount':user_wager, 'earned_payout':earned_payout, 'bet_status':bet_status}
                    st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
                    
            # Submitted bets dataframe
            st.session_state.df.index = sub_index
            st.dataframe(st.session_state.df)

        except:
            st.write("Error: We are working on this.")
        

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

###########################
# Admin Functions
###########################
admin_account = os.getenv("ADMIN_PUBLIC_KEY")

st.sidebar.markdown('## Administrator Functions')
with st.sidebar.form(key="update_bet"):
    st.markdown('### Update Earned Payout')
    # Updates earneed payout (Only the owner of the contract can run this function.)
    #update_betID = st.number_input("Enter a Bet Token ID to Update:", step=1)
    #new_earned_payout = st.number_input("Calculate Payout", min_value=0)
    #new_bet_status = st.selectbox("Bet Selection", options=status_list)
    winner_bet_selection = st.selectbox('Choose THE winner:', [Team_1, Team_2, "DNP"])
    loser_bet_selection = st.selectbox('Choose THE loser:', [Team_1, Team_2, "DNP"])
    submitted = submit_button = st.form_submit_button(label='Update Bet')
    if submitted:
        try:
            betID = (contract.functions.totalSupply().call()-1)
            index = range(0, betID+1)

            for n in index:
                user_name, user_bet_selection, user_wager, earned_payout, bet_status = contract.functions.reviewBet(n).call()
                if (winner_bet_selection == user_bet_selection):
                    new_earned_payout = 100
                    new_bet_status = "Winner"                
                    contract.functions.updateBet(n, new_earned_payout, new_bet_status).transact({'from': admin_account, 'gas': 1000000})  
                elif (loser_bet_selection == user_bet_selection):
                    new_earned_payout = 0
                    new_bet_status = "Loser"                
                    contract.functions.updateBet(n, new_earned_payout, new_bet_status).transact({'from': admin_account, 'gas': 1000000})          
        except:
            st.write("You do not have permission for this.")

with st.sidebar.form(key="withdraw_profit"):
    st.markdown('### Transfer Profits')
    amount = st.number_input("Enter Amount To Withdraw:", step=1)
    # Updates earneed payout (Only the owner of the contract can run this function.)
    submitted = submit_button = st.form_submit_button(label='Withdraw Profits')
    if submitted:
        try:
            contract.functions.transferProfits(amount, admin_account).transact({'from': admin_account, 'gas': 1000000})
        except:
            st.write("Not an authorized user.")


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


