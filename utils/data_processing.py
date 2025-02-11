import json
import pandas as pd

def load_and_process_data():
    with open('data/data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    all_players = []
    team_averages = []
    
    for team in data['teams']:
        team_name = team['name']
        for week in team['weeks']:
            week_num = week['week']
            for player in week['players']:
                player_data = {
                    'team': team_name,
                    'week': week_num,
                    'name': player['name'],
                    'lane': player['lane'],
                    'country': player['country'],
                    'score': player['score'],
                    'tier': player['tier']
                }
                all_players.append(player_data)
            team_averages.append({
                'team': team_name,
                'week': week_num,
                'average_score': week['average_score']
            })
    
    return pd.DataFrame(all_players), pd.DataFrame(team_averages)

def calculate_metrics(df_players, df_teams):
    metrics = []
    
    weeks = df_teams['week'].unique()
    
    for week in weeks:
        best_team = df_teams[df_teams['week'] == week].nlargest(1, 'average_score')['team'].values[0]
        
        if week == 1:
            best_player = df_players[df_players['week'] == week].nlargest(1, 'score')['name'].values[0]
        else:
            prev_week = df_players[df_players['week'] == week - 1].set_index(['name', 'team'])['score']
            curr_week = df_players[df_players['week'] == week].set_index(['name', 'team'])['score']
            improvement = (curr_week - prev_week).reset_index()
            best_player = improvement.nlargest(1, 'score')['name'].values[0]
        
        if week == 1:
            most_improved_team = "N/A"
        else:
            prev_week_avg = df_teams[df_teams['week'] == week - 1].set_index('team')['average_score']
            curr_week_avg = df_teams[df_teams['week'] == week].set_index('team')['average_score']
            team_improvement = (curr_week_avg - prev_week_avg).reset_index()
            most_improved_team = team_improvement.nlargest(1, 'average_score')['team'].values[0]
        
        metrics.append({
            'Semana': week,
            'Melhor Time': best_team,
            'Jogador com Maior Melhoria': best_player,
            'Time que Mais Evoluiu': most_improved_team
        })
    
    return pd.DataFrame(metrics)