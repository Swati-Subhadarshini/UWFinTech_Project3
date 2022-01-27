# Package Imports
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Function to pull the weekly odds.
def weekly_odds(dump):
    odds_df = pd.DataFrame()
    for i in range(len(dump)):
        t1 = pd.DataFrame(dump[i]['bookmakers'][1]['markets'][0]['outcomes'][0], index=[0])
        t1 = t1.rename(columns={'name':'t1_name','price':'t1_odds'})
        t2 = pd.DataFrame(dump[i]['bookmakers'][1]['markets'][0]['outcomes'][1], index=[0])
        t2 = t2.rename(columns={'name':'t2_name','price':'t2_odds'}) 
        t1['away_team'] = dump[i]['away_team']
        t1['home_team'] = dump[i]['home_team']
        joined_odds = pd.concat([t1, t2], axis='columns')
        odds_df = odds_df.append(joined_odds)
         
    return odds_df

# Create Variable for Odds APi Key
odds_api_key = os.getenv("ODDS_API")

# Define variables for pull requests
SPORT = 'americanfootball_nfl' # use the sport_key from the /sports endpoint, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'american' # decimal | american
DATE_FORMAT = 'iso' # iso | unix

# This cell will process the API Call and create an odds_response variable to be printed below.
# This does count towards the API usage count.
odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': odds_api_key,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
})
# Create object for API call.
if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    odds_json = odds_response.json()

# Use weekly_odds function & format results
upcoming_games = weekly_odds(odds_json)
upcoming_games = upcoming_games.reset_index().drop(columns='index')
first_column = upcoming_games.pop('away_team')
second_column = upcoming_games.pop('home_team')
upcoming_games.insert(0,'away_team',first_column)
upcoming_games.insert(1,'home_team',second_column)

# Export upcoming games to csv.
upcoming_games.to_csv("Resources/upcoming_games.csv")