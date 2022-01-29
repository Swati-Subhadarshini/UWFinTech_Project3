import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

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


################################################################################
# BET INPUTS
################################################################################
games_list = ["IMPORT", "GAMES", "HERE"]
accounts = w3.eth.accounts
#account = accounts[0]

st.markdown("### USER: Bet Parameters")

user_account = st.selectbox("Select Account", options=accounts)
username = st.text_input("Input Username")
bet_selection = st.selectbox("Bet Selection", options=games_list)
wager = st.number_input("Wager", min_value=0)

################################################################################
# USER FUNCTIONS
################################################################################

st.markdown("### USER: Place Bet")
if st.button("Place Bet"):
    try:
        earned_payout = 0
        contract.functions.placeBet(user_account, username, bet_selection).transact({'from': user_account, 'value': w3.toWei(wager,'wei'), 'gas': 1000000})
    except:
        st.write("Your bet is too large.")

st.markdown("### USER: Display Bet")
betID = st.number_input("Enter a Bet Token ID to display", value=0, step=1)
if st.button("Display Bet"):
    
    username, bet_selection, wager, earned_payout = contract.functions.reviewBet(betID).call()
    
    st.write(f"Username:{username}")
    st.write(f"Selected Bet:{bet_selection}")
    st.write(f"Wager:{wager} Wei")
    #st.write(f"Potential Payout:{potential_payout*1000000000000000000} Ether") #Add this in final streamlit app
    st.write(f"Earned Payout:{earned_payout} Wei")

st.markdown("### USER: Cashout")
if st.button("winnerCashout"):
    try:
        contract.functions.winnerCashout(betID, user_account).transact({'from': user_account, 'gas': 1000000})
    except:
        st.write("No access to this bet or you did not win.")

################################################################################
# OWNER ONLY FUNCTIONS
################################################################################

st.markdown("### Owner: Update Earned Payout")
# Updates earneed payout (Only the owner of the contract can run this function.)
new_earned_payout = st.number_input("Calculate Payout", min_value=0)
if st.button("updateBet"):
    try:
        contract.functions.updateBet(betID, new_earned_payout).transact({'from': user_account, 'gas': 1000000})
        earned_payout = new_earned_payout
    except:
        st.write("You do not have permission for this.")

# Allows for owner of the contract to transfer a set amount of money to their own account (Only the owner of the contract can run this function.)

st.markdown("### Owner: Withdraw Profit")
amount = st.number_input("Amount to withdraw:", min_value=0)

if st.button("transferProfits"):
    try:
        contract.functions.transferProfits(amount, user_account).transact({'from': user_account, 'gas': 1000000})
    except:
        st.write("Not an authorized user.")
