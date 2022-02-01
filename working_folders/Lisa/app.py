# Building a Blockchain Block
################################################################################
# In this activity, you’ll build a Streamlit application that accepts user
# input and then stores that input in a `Block` data class.

# The instructions for this activity are divided into the following high-level
# steps:
# 1. Create a data class for storing data from a user.
# 2. Create a Streamlit component to accept user input.
# 3. Create a button for storing and displaying the user input.
# 4. Test the application.

################################################################################
# Imports
import streamlit as st
from dataclasses import dataclass
from datetime import datetime
from datetime import date
import time
from typing import Any

import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
################################################################################
# Step 1:
# Create a Data Class for Storing Data from a User

# In this section, you’ll create a data class named `Block` for storing data
# from a user. To do so, complete the following steps:
# 1. Define a class named `Block` and add the `@dataclass` decorator.
# 2. Inside the data class, define an attribute named `data` with a type of
# `Any`.
# 3. Inside the data class, define an attribute named `creator_id` with a type
# of `int`.
# 4. Inside the data class, define an attribute name `timestamp` with a type of
# `str`.
# 5. Assign a default value to the `timestamp` attribute by using the following
# code: `datetime.utcnow().strftime("%H:%M:%S")`

# @TODO
# Define a class `Block` and add the `@dataclass` decorator.


@dataclass
class Block:
    # @TODO:
    # Define an attribute named `data` with a type of `Any`.
    data: Any
    # @TODO:
    # Define an attribute named `creator_id` with a type of `int`.
    creator_id: int
    # @TODO:
    # Define an attribute name `timestamp` with a type of `str`.
    # Use the following code to set the value:
    # `datetime.utcnow().strftime("%H:%M:%S")`
    timestamp: str = datetime.utcnow().strftime("%H:%M:%S")


# Create the application headers using markdown strings.
st.markdown("# Welcome to Blockchain Gambling")
st.markdown("## Place a bet on the Superbowl LVI winner")

team = st.radio('Select the team that you would like to bet will will Superbowl LVI', options=['Team A', 'Team B'])
'team: ', team
bet_amount = st.number_input('How much Ether would you like to bet?')
'bet amount: ', bet_amount

#st.markdown("Today is datetime.utcnow().strftime("%A %B %d %d%H:%M:%S")")
'Today is: ', datetime.now().strftime("%A %B %d %H:%M:%S")
'Today is: ', datetime.utcnow().strftime("%D/%M/%Y %H:%M:%S")

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/artwork_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()


################################################################################
# Register New Artwork
################################################################################
st.title("Place your bet")
accounts = w3.eth.accounts

"Bookee's address:", accounts[0]
'Betters', accounts[1:]

#better_address = st.text_input("Please enter the better's address: ")
better_address = st.selectbox("Please enter the better's address: ", options=accounts)
'better_address: ', better_address

# Use a streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select Artwork Owner", options=accounts)

# Use a streamlit component to get the artwork's URI
artwork_uri = st.text_input("The URI to the artwork")
artwork_uri = team

if st.button("Place Bet!"):

    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract.functions.registerArtwork(
        better_address,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display Bet  Token")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Artwork Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)

st.text('###########################################################')

st.text('Display interactive widgets')
st.button('Hit me')
st.download_button('download a file with the current time', datetime.utcnow().strftime("%H:%M:%S"))
st.checkbox('Check me out')
st.radio('Radio', [1,2,3])
st.selectbox('Select', [1,2,3])
st.multiselect('Multiselect', [1,2,3])
st.slider('Slide me', min_value=0, max_value=10)
st.select_slider('Slide to select', options=[1,'2'])
st.text_input('Enter some text')
st.number_input('Enter a number')
st.text_area('Area for textual entry')
st.date_input('Date input')
st.time_input('Time entry')
st.file_uploader('File uploader')
st.color_picker('Pick a color')

################################################################################
# Step 2:
# Create a Streamlit Component to Accept User Input

# @TODO:
# Referencing the Streamlit library, use the `text_input` function and pass the
# parameter "Block Data".
input_data = st.text_input("Block Data")

################################################################################
# Step 3:
# Create a Button for Storing and Displaying the User Input

# In this section, you’ll create a button that will store the user input in an
# instance of the `Block` data class and then display it to the user. To do so,
# complete the following steps:
# 1. Create a Streamlit `button`, and pass the “Add Block” parameter to it.
# 2. In the button statement, create an instance of the `Block` data class. Use
# the user input from the preceding “Step 2” section for the data attribute,
# and use the integer 42 for the creator ID.
# Hint: Create an instance of the Block dataclass using the following code:
# `new_block = Block(data=input_data, creator_id=42)`
# 3. Use the `st.write` function to display the new block.

# @TODO:
# Create a Streamlit `button`, and pass the “Add Block” parameter to it.
if st.button("Add Block"):
    # @TODO:
    # Create an instance of the `Block` data class called `new_block`
    # Use the user input from Step 2 for the `data` attribute
    # Use the integer 42 for the `creator_id`
    new_block = Block(data=input_data, creator_id=42)
    # @TODO:
    # Use the `st.write` function to display the new block.
    st.write(new_block)

################################################################################
# Step 4:
# Test the Application

# Complete the following steps:
# 1. In the terminal, navigate to the `Unsolved` folder for this activity.
# 2. Run the Streamlit app in the terminal by using `streamlit run app.py`.
# 3. Store some data in a block by using the Streamlit input box.
# 4. Click the Add Block button, and then check that the new block displays on
# the page.

################################################################################
