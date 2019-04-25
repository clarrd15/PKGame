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
