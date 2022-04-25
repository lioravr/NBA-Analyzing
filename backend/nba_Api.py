from math import exp
import pandas as pd


BASE_URL = 'https://www.basketball-reference.com/'
ADVANCED_BOX_SCORE_COLS = ['Player','Pos','Tm','Scoring Rate','Efficiency(TS%)','Spacing','Creation','Offensive Load']

def load_data(year: int, standing_type: str):
    if standing_type == 'play-by-play':
        return get_players_data(year, standing_type, 1)
    elif standing_type == 'advanced_box_score':
        return get_advanced_metrics(year)
    return get_players_data(year, standing_type)



def get_players_data(season: int, standing_type: str, header: int = 0, filter_games=True, remove_duplicates=True):
    """
    Returns a dataframe representing player data from the season and stat type selected web scrapping basketball reference website
    """
    url = f'{BASE_URL}leagues/NBA_{str(season)}_{standing_type}.html'
    html = pd.read_html(url, header = header)
    df = html[0]

    raw = None
    if 'Age' in df:
        raw = df.drop(df[df.Age == 'Age'].index)
        raw = raw.fillna(0)
    
    player_standing = raw.drop(['Rk'], axis=1) if raw is not None else df.drop(['Rk'])

    cols=[i for i in player_standing.columns if i not in ['Player','Pos', 'Tm']]
    for col in cols:
        try:
            player_standing[col]=pd.to_numeric(player_standing[col])
        except ValueError:
            player_standing[col]=player_standing[col]
    
    if filter_games:
        max_games_played = player_standing['G'].max()
        threshold = max_games_played // 2   
        player_standing = player_standing[player_standing['G'] >= threshold]

    if remove_duplicates:
        player_standing.drop_duplicates(subset=['Player'], inplace=True)
        player_standing['Pos'].replace(['SG-PG','SG-SF','SG-PF','SG-C'], 'SG', inplace=True)        
        player_standing['Pos'].replace(['PG-SG','PG-SF','PG-PF','PG-C'], 'PG', inplace=True)
        player_standing['Pos'].replace(['SF-PG','SF-SG','SF-PF','SF-C'], 'SF', inplace=True)
        player_standing['Pos'].replace(['PF-PG','PF-SF','PF-SF','PF-C'], 'PF', inplace=True)
        player_standing['Pos'].replace(['C-PG','C-SF','C-PF','C-SG'], 'C', inplace=True)        
        
    return player_standing



def get_advanced_metrics(season: int):
    per_100 = get_players_data(season, 'per_poss')
    advanced = get_players_data(season, 'advanced')
    per_game = get_players_data(season, 'per_game')
    league_avg_efg = per_game['eFG%'].mean()

    table = [[p,pos,tm,pts,ts,spacing(attmpts,pctg,league_avg_efg),box_creation(ast,pts,attmpts,pctg,tov),offensive_load(ast,fga,fta,tov,box_creation(ast,pts,attmpts,pctg,tov))] 
        for p,pos,tm,pts,ts,attmpts,pctg,ast,tov,fga,fta 
        in zip(per_100['Player'],per_100['Pos'],per_100['Tm'],per_100['PTS'],advanced['TS%'],per_100['3PA'],per_100['3P%'],per_100['AST'],per_100['TOV'],per_100['FGA'],per_100['FTA'])]
    return pd.DataFrame(table, columns=ADVANCED_BOX_SCORE_COLS)    

def box_creation(ass_per_100: float, pts_per_100: float, attempts: float, percentage: float, turnovers_per_100: float):
    """
    A per 100 estimate of the number of \'true\' shots created for teammates
    """
    proficiency = shooting_proficiency(attempts, percentage)
    return ass_per_100*0.1843+(pts_per_100+turnovers_per_100)*0.0969-2.3021*(proficiency)+0.0582*(ass_per_100*(pts_per_100+turnovers_per_100)*proficiency)-1.1942

def offensive_load(ass: float, field_goals: float, free_throws: float, turnovers: float, box_creation: float):
    """
    The percentage of possessions a player is directly or indirectly involved in a true shooting attempt, or commits a turnover.
    """
    return ((ass-(0.38*box_creation))*0.75) + field_goals + free_throws*0.44 + box_creation + turnovers

def shooting_proficiency(attempts: float, percentage: float):
    """
    A measure of shooting quality that takes into account both attempts as well as accuracy.
    """
    return (2/(1+exp(-attempts))-1)*percentage

def spacing(attemps: float, percentage: float, league_avg_efg: float):
    """
    (3PA * (3P% * 1.5)) - EFG% =
    A measure of shooting quality that takes into account both attempts as well as accuracy, with a slight adjustment towards attempts.
    """
    return (attemps * (percentage * 1.5)) - league_avg_efg

