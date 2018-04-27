# -*- coding: UTF-8 -*-
import csv

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

RATING_CONFIG = {
    'shotsAccuracyRating': {}
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


def calculate_scores(file_name, calculator_config=CONFIG):
    # stats keys:
    # [u'cornersTotal', u'aerialsWon', u'dribblesLost', u'shotsTotal', u'passesAccurate',
    # u'tackleUnsuccesful', u'defensiveAerials', u'aerialsTotal', u'offensiveAerials',
    # u'passesTotal', u'throwInsTotal', u'dispossessed', u'interceptions', u'ratings',
    # u'touches', u'offsidesCaught', u'parriedSafe', u'clearances', u'throwInAccuracy',
    # u'collected', u'parriedDanger', u'possession', u'shotsOffTarget', u'dribblesAttempted',
    # u'dribblesWon', u'cornersAccurate', u'tackleSuccess', u'throwInsAccurate', u'dribbleSuccess',
    # u'errors', u'aerialSuccess', u'tacklesTotal', u'tackleSuccessful', u'shotsOnTarget',
    # u'passesKey', u'dribbledPast', u'foulsCommited', u'shotsBlocked', u'totalSaves', u'passSuccess']
    with open(file_name, "r") as theFile:
        reader = csv.DictReader(theFile)
        calculate(reader, calculator_config=calculator_config)


def calculate(reader, calculator_config=CONFIG):
    results = []
    for line in reader:
        team, name, position, id = line['team'], line['name'], line['position'], line['id']
        xtPosition = position
        result = {}
        if float(line['playMins']) > 0:
            for new_key, keys in COMBINED_KEYS.items():
                line[new_key] = sum([float(line[key]) for key in keys])
            for new_key, (success_key, total_key) in PERCENT_KEYS.items():
                line[new_key] = safe_division(float(line[success_key]), float(line[total_key]))

        for rating_key, config in calculator_config[xt_position(position)].items():
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
        result.update(
            {'id': id, 'team': team, 'name': name, 'position': position, 'xtPosition': xtPosition})
        results.append(result)
    return {'Done': len(results)}
