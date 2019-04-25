import nashpy as nash
import numpy as np
import os

def NashEq(KickerPayoffs, GoaliePayoffs):
    pk = nash.Game(KickerPayoffs, GoaliePayoffs)
    NashEq = list(pk.support_enumeration())
    KickerNaturalProb = NashEq[0][0][0]
    GoalieNaturalProb = NashEq[0][1][0]
    return KickerNaturalProb, GoalieNaturalProb

def print_to_file(player_goals, CPU_goals, result):
    exists = os.path.isfile('results.dat')
    if exists:
        results = open('results.dat', 'a')
        results.write('%d, %d, %s\n' % (player_goals, CPU_goals, result))
        results.close()
    else:
        results = open('results.dat', 'w+')
        results.write('Player Goals, CPU Goals, Winner\n')
        results.write('%d, %d, %s\n' % (player_goals, CPU_goals, result))
        results.close()
    print('Results saved! Come back soon!')
