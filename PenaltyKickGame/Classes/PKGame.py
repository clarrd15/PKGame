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
