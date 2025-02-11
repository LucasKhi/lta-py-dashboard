import json
import pandas as pd
import numpy as np

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
    
    # Lista de semanas disponíveis
    weeks = df_teams['week'].unique()
    
    # Mapeamento para converter tiers em valores numéricos
    tier_mapping = {"bagre": 1, "mediano": 2, "bom": 3, "craque": 4, "god": 5}
    
    for week in weeks:
        # Dados da semana atual
        week_teams = df_teams[df_teams['week'] == week]
        week_players = df_players[df_players['week'] == week]
        
        # Melhor time da semana (maior média)
        best_team = week_teams.nlargest(1, 'average_score', 'all')['team'].values[0] if not week_teams.empty else "N/A"
        
        # Pior time da semana (menor média)
        worst_team = week_teams.nsmallest(1, 'average_score', 'all')['team'].values[0] if not week_teams.empty else "N/A"
        
        # Jogador com maior melhoria na pontuação
        if week == 1:
            best_player = week_players.nlargest(1, 'score', 'all')['name'].values[0] if not week_players.empty else "N/A"
        else:
            prev_week = df_players[df_players['week'] == week - 1].set_index(['name', 'team'])['score']
            curr_week = df_players[df_players['week'] == week].set_index(['name', 'team'])['score']
            improvement = (curr_week - prev_week).fillna(0).reset_index()
            best_player = improvement.nlargest(1, 'score', 'all')['name'].values[0] if not improvement.empty else "N/A"
        
        # Jogador com pior desempenho (menor pontuação)
        worst_player = week_players.nsmallest(1, 'score', 'all')['name'].values[0] if not week_players.empty else "N/A"
        
        # Time que mais evoluiu (maior aumento na média)
        if week == 1:
            most_improved_team = "N/A"
        else:
            prev_week_avg = df_teams[df_teams['week'] == week - 1].set_index('team')['average_score']
            curr_week_avg = df_teams[df_teams['week'] == week].set_index('team')['average_score']
            team_improvement = (curr_week_avg - prev_week_avg).fillna(0).reset_index()
            most_improved_team = team_improvement.nlargest(1, 'average_score', 'all')['team'].values[0] if not team_improvement.empty else "N/A"
        
        # Time com maior queda (menor aumento na média)
        if week == 1:
            most_declined_team = "N/A"
        else:
            team_decline = (curr_week_avg - prev_week_avg).fillna(0).reset_index()
            most_declined_team = team_decline.nsmallest(1, 'average_score', 'all')['team'].values[0] if not team_decline.empty else "N/A"
        
        # Jogador mais consistente (menor variação de pontuação)
        if week == 1:
            most_consistent_player = "N/A"
        else:
            player_variation = df_players[df_players['week'].isin([week - 1, week])].groupby(['name', 'team'])['score'].std().reset_index()
            player_variation.dropna(inplace=True)
            most_consistent_player = player_variation.nsmallest(1, 'score', 'all')['name'].values[0] if not player_variation.empty else "N/A"
        
        # Time mais consistente (menor variação na média)
        if week == 1:
            most_consistent_team = "N/A"
        else:
            team_variation = df_teams[df_teams['week'].isin([week - 1, week])].groupby('team')['average_score'].std().reset_index()
            team_variation.dropna(inplace=True)
            most_consistent_team = team_variation.nsmallest(1, 'average_score', 'all')['team'].values[0] if not team_variation.empty else "N/A"
        
        # Maior queda de desempenho (jogador que perdeu mais pontos)
        if week == 1:
            biggest_drop_player = "N/A"
        else:
            drop = (prev_week - curr_week).fillna(0).reset_index()
            biggest_drop_player = drop.nlargest(1, 'score', 'all')['name'].values[0] if not drop.empty else "N/A"
        
        # Melhor jogador por lane
        best_players_by_lane = week_players.loc[week_players.groupby('lane')['score'].idxmax(), ['lane', 'name']]
        best_players_by_lane = ", ".join([f"{p['lane']}: {p['name']}" for p in best_players_by_lane.to_dict('records')]) if not best_players_by_lane.empty else "N/A"
        
        # Melhor jogador geral (maior pontuação em todas as semanas)
        best_player_overall = df_players.nlargest(1, 'score', 'all')['name'].values[0] if not df_players.empty else "N/A"
        
        # Time com melhor rendimento por nacionalidade
        nationality_avg = df_players.groupby(['team', 'country'])['score'].mean().reset_index()
        best_nationality_team = nationality_avg.nlargest(1, 'score', 'all')['team'].values[0] if not nationality_avg.empty else "N/A"
        
        # Evolução de tiers
        if week == 1:
            tier_evolution = "N/A"
        else:
            df_players['tier_numeric'] = df_players['tier'].map(tier_mapping).fillna(0)
            tier_change = df_players[df_players['week'].isin([week - 1, week])].groupby(['name', 'team'])['tier_numeric'].nunique().reset_index()
            tier_evolution = tier_change[tier_change['tier_numeric'] > 1].shape[0] if not tier_change.empty else "N/A"
        
        # Adicionar métricas à lista
        metrics.append({
            'Semana': f"Semana {week}",
            'Melhor Time': best_team,
            'Pior Time': worst_team,
            'Jogador com Maior Melhoria': best_player,
            'Jogador com Pior Desempenho': worst_player,
            'Time que Mais Evoluiu': most_improved_team,
            'Time com Maior Queda': most_declined_team,
            'Jogador Mais Consistente': most_consistent_player,
            'Time Mais Consistente': most_consistent_team,
            'Maior Queda de Desempenho': biggest_drop_player,
            'Melhores Jogadores por Lane': best_players_by_lane,
            'Melhor Jogador Geral': best_player_overall,
            'Time com Melhor Rendimento por Nacionalidade': best_nationality_team,
            'Evolução de Tiers': tier_evolution
        })
    
    return pd.DataFrame(metrics)