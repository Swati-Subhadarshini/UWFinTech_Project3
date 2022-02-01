from re import A
import pandas as pd
import streamlit as st

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['user_address', 'user_name', 'bet_selection', 'wager_amount'])

st.dataframe(st.session_state.df)

Team_1 = "A"
Team_2 = "B"

with st.form(key='place_bet'):
    user_address = st.text_input('Enter your public address')
    user_name = st.text_input('Enter your UserName')
    user_bet_selection = st.selectbox('Choose YOUR winner:', [Team_1, Team_2])
    user_wager = st.number_input('Wager Amount', min_value=0)

    submitted = submit_button = st.form_submit_button(label='Submit Bet')
    if submitted:
        new_row = {'user_address':user_address, 'user_name':user_name, 'bet_selection':user_bet_selection, 'wager_amount':user_wager}
        st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
st.dataframe(st.session_state.df)



'''data = []

columns = ['user_address', 'user_name', 'wager_amount', 'bet_selection']
df =  pd.DataFrame(columns=columns)

address = '1xasd1234101'
username = 'ballbailey'
bet_amount = 20
bet_team = 'Team B'

new_row = {'user_address': '902', 'user_name': 'balllisaann2', 'wager_amount': 2, 'bet_selection': 'Team a'}
df = df.append(new_row, ignore_index=True)

new_row = {'user_address': '902', 'user_name': 'balllisaann2', 'wager_amount': 2, 'bet_selection': 'Team a'}
df = df.append(new_row, ignore_index=True)

print(df)'''