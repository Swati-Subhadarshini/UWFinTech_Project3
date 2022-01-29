import pandas as pd
data = []

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

print(df)