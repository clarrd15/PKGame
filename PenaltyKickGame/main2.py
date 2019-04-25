import nashpy as nash
import numpy as np
import os

class Player:
    def __init__(self):
        self.foot = 'none'
        self.oppfoot = 'none'
        self.goals = 0
        self.turn = True
        self.kicks_remaining = 5

    def pkResult(self, KickerChoice, GoalieChoice):
        if KickerChoice == 'N' and GoalieChoice == 'N':
            GoalProb = KickerPayoffs[0][0] / 100
            NoGoalProb = 1 - GoalProb
            outcome = np.random.choice(['Goal', 'No Goal'],p=[GoalProb,NoGoalProb])
        elif KickerChoice == 'N' and GoalieChoice == 'Opp':
            GoalProb = KickerPayoffs[0][1] / 100
            NoGoalProb = 1 - GoalProb
            outcome = np.random.choice(['Goal','No Goal'],p=[GoalProb, NoGoalProb])
        elif KickerChoice == 'Opp' and GoalieChoice == 'N':
            GoalProb = KickerPayoffs[1][0] / 100
            NoGoalProb = 1 - GoalProb
            outcome = np.random.choice(['Goal','No Goal'],p=[GoalProb, NoGoalProb])
        elif KickerChoice == 'Opp' and GoalieChoice == 'Opp':
            GoalProb = KickerPayoffs[1][1] / 100
            NoGoalProb = 1 - GoalProb
            outcome = np.random.choice(['Goal','No Goal'],p=[GoalProb, NoGoalProb])
        if outcome == 'Goal':
            self.goals += 1
        return outcome, self.goals

class PKGame:
    def __init__(self):
        self.done = False
        self.player = Player()
        self.CPU = Player()
        self.round = 1
        self.winner = 'none'

    def game(self):
        # Game Info
        print('Welcome to Penalty Kick Simulator!\n')
        print('Rules: Player and CPU have 5 kicks. At the end of these 5, whomever has more goals wins. If there are not enough turns for a player or CPU to come back, game finishes. If tied at the end of 5 rounds, play keeps going 1 at a time until a winner is decided. The CPU will always act according to the Nash Equilibrium Probabilities for the kicker and goalie.')
        print('\nTime for Penalty Kicks! Player kicks first.')
        self.player.foot = input('\nAre you left or right footed? Type R or L:\n')
        if self.player.foot == 'R':
            print('Your natural side to kick towards is left')
            self.player.oppfoot = 'L'
        elif self.player.foot == 'L':
            print('Your natural side to kick towards is right.')
            self.player.oppfoot = 'R'

        # Play Game
        while not self.done:
            if (self.player.goals - self.CPU.goals) > self.CPU.kicks_remaining or (self.CPU.goals - self.player.goals) > self.player.kicks_remaining:
                done = True
                if self.player.goals > self.CPU.goals:
                    self.winner = 'Player'
                else:
                    self.winner = 'CPU'
                print('\nGame over! %s wins!' % self.winner)
                break
            elif self.player.kicks_remaining == 0 and self.CPU.kicks_remaining == 0:
                print('Tied at the end of %d rounds! Play will continue 1 round at a time until a winner is decided.' % self.rounds)
                self.player.kicks_remaining += 1
                self.CPU.kicks_remaining += 1
            if self.player.turn:
                print('-------------------')
                print ('Round %d!' % self.round)
                KickerChoice = input('Would you like to kick Right(R) or Left(L)?:\n')
                if KickerChoice == self.player.foot:
                    KickerChoice = 'N'
                else:
                    KickerChoice = 'Opp'
                GoalieChoice = np.random.choice(['N','Opp'],p=[GoalieNaturalProb, GoalieOppositeProb])
                result, player_goals = self.player.pkResult(KickerChoice, GoalieChoice)
                if GoalieChoice == 'N':
                    GoalieChoice = self.player.foot
                else:
                    GoalieChoice = self.player.oppfoot
                    
                print('Goalie chose %s. %s! Update: Player Goals = %d, CPU Goals = %d' % (GoalieChoice, result, player_goals, self.CPU.goals))
                self.player.turn = False
                self.player.kicks_remaining -= 1
            else:
                KickerChoice = np.random.choice(['N','Opp'],p=[KickerNaturalProb, KickerOppositeProb])
                GoalieChoice = input('CPU is kicking! Do you jump towards their natural side (L) or opposite side (R)?:\n')
                if GoalieChoice == 'L':
                    GoalieChoice = 'N'
                else:
                    GoalieChoice = 'Opp'
                result, CPU_goals = self.CPU.pkResult(KickerChoice, GoalieChoice)
                if KickerChoice == 'N':
                    KickerChoice = 'L'
                else:
                    KickerChoice = 'R'
                print('CPU chose %s. %s! Update: Player Goals = %d, CPU Goals = %d' % (KickerChoice, result, self.player.goals, CPU_goals))
                self.player.turn = True
                self.CPU.kicks_remaining -= 1
                self.round += 1
        return self.player.goals, self.CPU.goals, self.winner

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
    
if __name__ == '__main__':
    # Create game using payoffs from dataset
    KickerPayoffs = np.array([[63.6,94.6],[89.3,43.7]])
    GoaliePayoffs = 100-KickerPayoffs    

    # Define probabilities for Kicker and Goalie using the results of the Nash Eq Calculation
    KickerNaturalProb, GoalieNaturalProb = NashEq(KickerPayoffs, GoaliePayoffs)
    KickerOppositeProb = 1 - KickerNaturalProb
    GoalieOppositeProb = 1 - GoalieNaturalProb
    
    # Create game and let it run
    PKGame = PKGame()
    player_goals, CPU_goals, winner = PKGame.game()
    print_to_file(player_goals, CPU_goals, winner)
    
