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
# Award Certificate
################################################################################
games_list = ["IMPORT", "GAMES", "HERE"]
accounts = w3.eth.accounts
#account = accounts[0]
user_account = st.selectbox("Select Account", options=accounts)
username = st.text_input("Input Username")
bet_selection = st.selectbox("Bet Selection", options=games_list)
wager = st.number_input("Wager", min_value=0)
st.markdown("## Potential Payout")
potential_payout = wager*2
st.write(potential_payout)

if st.button("Place Bet"):
    earned_payout = 0
    contract.functions.placeBet(user_account, username, bet_selection).transact({'from': user_account, 'value': w3.toWei(wager,'ether'), 'gas': 1000000})

################################################################################
# Display Bet Slip
################################################################################
betID = st.number_input("Enter a Bet Token ID to display", value=0, step=1)
if st.button("Display Bet"):
    # Get the certificate owner
    username, bet_selection, wager, potential_payout, earned_payout = contract.functions.reviewBet(betID).call()
    
    st.write(f"Username:{username}")
    st.write(f"Selected Bet:{bet_selection}")
    st.write(f"Wager:{wager/(1000000000000000000)} Ether")
    st.write(f"Potential Payout:{potential_payout} Ether")
    st.write(f"Earned Payout:{earned_payout} Ether")

    # Get the certificate's metadata
    #certificate_uri = contract.functions.tokenURI(certificate_id).call()
    #st.write(f"The certificate's tokenURI metadata is {certificate_uri}")
