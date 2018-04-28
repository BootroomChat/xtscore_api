# -*- coding: UTF-8 -*-

import pandas as pd

from xt_config import *
from xt_util import *

COMBINED_KEYS = {
    'defenseThree': ['interceptions', 'tackleSuccessful', 'clearances'],
    'totalErrors': ['errorsCount', 'penaltyConceded'],
    'cccPasses': ['passesKey', 'assists', 'assists'],
    'totalCollected': ['collected', 'claimsHigh'],
    'totalParried': ['parriedDanger', 'parriedSafe'],
}
PERCENT_KEYS = {
    'aerialSuccess': ['aerialsWon', 'aerialsTotal'],
    'shotsAccuracy': ['shotsOnTarget', 'shotsTotal'],
    'passesAccuracy': ['passesAccurate', 'passesTotal'],
}


def xt_position(position):
    if position in ['FW', 'FWL', 'FWR', 'AML', 'AMR']:
        return 'FW'
    elif position in ['AMC', 'SS']:
        return 'AMC/SS'
    elif position in ['WF', 'IF']:
        return 'WF/IF'
    elif position in ['CM', 'LCM', 'RCM', 'MC', 'ML', 'MR']:
        return 'CM/LCM/RCM'
    elif position in ['DM', 'DMC', 'DML', 'DMR']:
        return 'DM'
    elif position in ['DL', 'DR']:
        return 'DL/DR'
    else:
        return position


def calculate(reader, calculator_config=CONFIG):
    results = []
    for line in reader:
        line = line.copy()
        xtPosition = xt_position(line['position'])
        result = {}
        if float(line['playMins']) > 0:
            for new_key, keys in COMBINED_KEYS.items():
                line[new_key] = sum([float(line[key]) for key in keys])
            for new_key, (success_key, total_key) in PERCENT_KEYS.items():
                line[new_key] = safe_division(float(line[success_key]), float(line[total_key]))

        for rating_key, config in calculator_config[xtPosition].items():
            if config['function'] != 'zero':
                value = float(line[config['key']])
                if config['per_mode'] == '_minute':
                    value = (float(line[config['key']])) * 90 / float(line['playMins'])
                elif config['per_mode'] == 'minute':
                    value = (float(line[config['key']])) / 90 * float(line['playMins'])

                if config['function'] == 'normdist':
                    result[rating_key] = normdist(value, float(config['params'][0]), float(config['params'][1]),
                                                  True) * float(config['percent']) * 100
                elif config['function'] == 'multiply':
                    result[rating_key] = value * float(config['params']) * float(config['percent'])
                elif config['function'] == 'minus_multiply':
                    result[rating_key] = float(config['percent']) * 100 - value * float(config['params'])

        result['overallRating'] = sum(result.values()) / 10 + 0
        result['adjustedRating'] = result['overallRating'] * 0.4
        line.update(result)
        line.update(
            {'xtPosition': xtPosition, 'playMins': line['playMins'], 'result': float(line['result']),
             'points': float(line['points'])})
        results.append(line)
    response_dict = {}
    data = pd.DataFrame(results)
    data = data[data['xtPosition'] != 'Sub']
    data['name_with_pos'] = data['name'] + ', ' + data['xtPosition'] + ', ' + data['team']
    scores = data[data['team'] == 'Liverpool'][
        ['team', 'name_with_pos', 'xtPosition', 'position', 'playMins', 'overallRating', 'result', 'points']]

    position_scores_agg = scores.groupby(['xtPosition'])[
        ['overallRating', 'result', 'points']].apply(position_agg)
    position_scores_agg.reset_index(level=0, inplace=True)

    response_dict['position_scores_agg'] = position_scores_agg.to_dict('records')

    team_scores_agg = data.groupby(['team'])[['overallRating', 'result', 'points']].mean()
    team_scores_agg.reset_index(level=0, inplace=True)
    response_dict['team_scores_agg'] = team_scores_agg.to_dict('records')

    player_scores_agg = scores.groupby(['name_with_pos'])[
        ['overallRating', 'result', 'points']].apply(
        player_agg).query('matches >= 10')
    player_scores_agg.reset_index(level=0, inplace=True)
    response_dict['player_scores_agg'] = player_scores_agg.to_dict('records')
    # response_dict['best_20_players_by_xts'] = player_scores_agg.sort_values(
    #     by=['overallRating'], ascending=False).head(20).to_dict('records')
    # response_dict['worst_20_players_by_xts'] = player_scores_agg.sort_values(
    #     by=['overallRating'], ascending=True).head(20).to_dict('records')
    # response_dict['best_20_players_by_points'] = player_scores_agg.sort_values(
    #     by=['points'], ascending=False).head(20).to_dict('records')
    # response_dict['worst_20_players_by_points'] = player_scores_agg.sort_values(
    #     by=['points'], ascending=True).head(20).to_dict('records')
    return response_dict


def position_agg(x):
    data = {'overallRating': x['overallRating'].mean(),
            'overallRatingStd': x['overallRating'].std(),
            'result': x['result'].mean(),
            'points': x['points'].mean(),
            'matches': x['result'].count()}
    return pd.Series(data)


def player_agg(x):
    data = {'overallRating': x['overallRating'].mean(),
            'overallRatingStd': x['overallRating'].std(),
            'result': x['result'].mean(),
            'points': x['points'].mean(),
            'matches': x['result'].count()}
    return pd.Series(data)
