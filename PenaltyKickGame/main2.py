from Classes.PKGame import *
from Classes.Player import *
from functions import *
    
if __name__ == '__main__':
    # Create game using payoffs from dataset
    KickerPayoffs = np.array([[63.6,94.6],[89.3,43.7]])
    GoaliePayoffs = 100 - KickerPayoffs    

    # Define probabilities for Kicker and Goalie using the results of the Nash Eq Calculation
    KickerNaturalProb, GoalieNaturalProb = NashEq(KickerPayoffs, GoaliePayoffs)
    KickerOppositeProb = 1 - KickerNaturalProb
    GoalieOppositeProb = 1 - GoalieNaturalProb
    
    # Create game and let it run
    PKGame = PKGame()
    player_goals, CPU_goals, winner = PKGame.game()
    print_to_file(player_goals, CPU_goals, winner)
    
