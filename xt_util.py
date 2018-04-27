from math import *

STATS_KEYS = [u'id', u'team', u'name', u'position', u'playMins', u'result', u'goals', u'assists', u'goalsConceded',
              u'penaltyConceded',
              u'cornersTotal', u'aerialsWon', u'dribblesLost', u'shotsTotal', u'passesAccurate', u'tackleUnsuccesful',
              u'defensiveAerials', u'aerialsTotal', u'offensiveAerials', u'passesTotal', u'throwInsTotal',
              u'offsidesCaught', u'interceptions', u'ratings', u'touches', u'dispossessed', u'parriedSafe',
              u'claimsHigh',
              u'clearances', u'throwInAccuracy', u'collected', u'parriedDanger', u'possession', u'shotsOffTarget',
              u'dribblesAttempted',
              u'shotsOnPost', u'dribblesWon', u'cornersAccurate', u'tackleSuccess', u'throwInsAccurate',
              u'dribbleSuccess', u'errorsCount',
              u'aerialSuccess', u'shotsBlocked', u'tacklesTotal', u'tackleSuccessful', u'shotsOnTarget',
              u'dribbledPast',
              u'passesKey', u'foulsCommited', u'totalSaves', u'passSuccess', u'claimsTotal']

RATING_KEYS = ['id', 'team', 'name', 'position', 'xtPosition', 'adjustedRating', 'overallRating', 'parriedDangerRating',
               'cccPassesRating', 'shotsAccuracyRating',
               'errorsRating', 'goalsConcededRating', 'dribbleSuccessRating', 'aerialSuccessRating', 'collectedRating',
               'totalSavesRating', 'dribbledPastRating', 'goalsRating', 'defenseThreeRatting', 'passesAccuracyRating']


def safe_division(a, b):
    if b == 0:
        return 0
    else:
        return a / b


def erfcc(x):
    """Complementary error function."""
    z = abs(x)
    t = 1. / (1. + 0.5 * z)
    r = t * exp(-z * z - 1.26551223 + t * (1.00002368 + t * (.37409196 +
                                                             t * (.09678418 + t * (-.18628806 + t * (.27886807 +
                                                                                                     t * (
                                                                                                             -1.13520398 + t * (
                                                                                                             1.48851587 + t * (
                                                                                                             -.82215223 +
                                                                                                             t * .17087277)))))))))
    if (x >= 0.):
        return r
    else:
        return 2. - r


def normcdf(x, mu, sigma):
    t = x - mu
    y = 0.5 * erfcc(-t / (sigma * sqrt(2.0)))
    if y > 1.0:
        y = 1.0
    return y


def normpdf(x, mu, sigma):
    u = (x - mu) / abs(sigma)
    y = (1 / (sqrt(2 * pi) * abs(sigma))) * exp(-u * u / 2)
    return y


def normdist(x, mu, sigma, f):
    if f:
        y = normcdf(x, mu, sigma)
    else:
        y = normpdf(x, mu, sigma)
    return y
