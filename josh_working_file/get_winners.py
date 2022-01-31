from sportsipy.nfl.boxscore import Boxscores, Boxscore
import pandas as pd

# Function will take the week & year of NFL season and return matchups and results (if finished).
def get_week_schedule(week, year):
    date_string = str(week) + '-' + str(year)
    week_scores = Boxscores(week,year)
    week_games_df = pd.DataFrame()
    for g in range(len(week_scores.games[date_string])):
        game = pd.DataFrame(week_scores.games[date_string][g], index = [0])[['away_name', 'away_abbr','away_score','home_name', 'home_abbr','home_score','winning_name', 'winning_abbr' ]]
        game['week'] = week
        week_games_df = pd.concat([week_games_df, game])
    return week_games_df

    