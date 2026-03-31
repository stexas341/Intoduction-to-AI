# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldGhostStates = currentGameState.getGhostStates()
        oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
        score = 0
        nearest_ghost = []
        for ghost in oldGhostStates:
          nearest_ghost += [manhattanDistance(ghost.configuration.pos, newPos)]

        NFood = newFood.asList()
        if len(NFood) == 0 :
          return successorGameState.getScore()

        #other_line = NFood[0]
        food = NFood[0]
        nearest_food = manhattanDistance(newPos, food)
        for f in NFood:
          temp = manhattanDistance(newPos, f)
          if temp < nearest_food:
            nearest_food = temp
        
      

        
        
        if action == 'Stop':
            score -= 50

        i = len(NFood)
        for t in range(0, len(oldScaredTimes)):
          if oldScaredTimes[t] != 0:
            score += ((nearest_ghost[t]/(nearest_food*50))- (nearest_food/2000)) - nearest_ghost[t]/4
          else:
            if nearest_ghost[t] <= 1.0:
              score += ((nearest_ghost[t]/(nearest_food*20))- nearest_food/100)  - (nearest_ghost[t]*1200)
            else:
              score += ((nearest_ghost[t]/(nearest_food*10))- nearest_food/3000)
              

       
        
        return successorGameState.getScore() + score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        fin_res = self.control(gameState, 0, 0)
        
        return fin_res[1] 

    def control(self, gameState, index, depth):
        if len(gameState.getLegalActions(index)) == 0 or gameState.isLose() or gameState.isWin() or depth == self.depth:
          return self.evaluationFunction(gameState), ""
          
        if index == 0:
          return self.max_act(gameState, index, depth)
        else:
          return self.min_act(gameState, index, depth)


    def max_act(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""
          

        for action in moves:
          successor = gameState.generateSuccessor(index, action)
          new_index = index + 1
          new_depth = depth
          
          if new_index == gameState.getNumAgents():
            new_index = 0
            new_depth += 1

          min_agent = self.control(successor, new_index, new_depth)

          if min_agent[0] > max_value:
            max_value = min_agent[0]
            max_action = action

        return max_value, max_action

    def min_act(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)
        min_value = float("inf")
        min_action = ""

        for action in moves:

          successor = gameState.generateSuccessor(index, action)
          new_index = index + 1
          new_depth = depth
          
          if new_index == gameState.getNumAgents():
            new_index = 0
            new_depth += 1

          max_agent = self.control(successor, new_index, new_depth)

          if max_agent[0] < min_value:
            min_value = max_agent[0]
            min_action = action

        return min_value, min_action   
        #util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        fin_res = self.control_ab(gameState, 0, 0, float("-inf"), float("inf"))
        
        return fin_res[1] 

    def control_ab(self, gameState, index, depth, alpha, beta):
        if len(gameState.getLegalActions(index)) == 0 or gameState.isLose() or gameState.isWin() or  depth == self.depth:
          return self.evaluationFunction(gameState), ""
          
        if index == 0:
          return self.max_act(gameState, index, depth, alpha, beta)
        else:
          return self.min_act(gameState, index, depth, alpha, beta)


    def max_act(self, gameState, index, depth, alpha, beta):
        moves = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""
          

        for action in moves:
          successor = gameState.generateSuccessor(index, action)
          new_index = index + 1
          new_depth = depth
          
          if new_index == gameState.getNumAgents():
            new_index = 0
            new_depth += 1

          min_agent = self.control_ab(successor, new_index, new_depth, alpha, beta)

          if min_agent[0] > max_value:
            max_value = min_agent[0]
            max_action = action

          if max_value > beta:
            return max_value, max_action

          alpha = max(alpha, max_value)


        return max_value, max_action

    def min_act(self, gameState, index, depth, alpha, beta):
        moves = gameState.getLegalActions(index)
        min_value = float("inf")
        min_action = ""

        for action in moves:

          successor = gameState.generateSuccessor(index, action)
          new_index = index + 1
          new_depth = depth
          
          if new_index == gameState.getNumAgents():
            new_index = 0
            new_depth += 1

          max_agent = self.control_ab(successor, new_index, new_depth, alpha, beta)

          if max_agent[0] < min_value:
            min_value = max_agent[0]
            min_action = action

          if min_value < alpha:
            return min_value, min_action

          beta = min(beta, min_value)

        return min_value, min_action       
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """
        "*** YOUR CODE HERE ***"

        fin_res = self.control(gameState, 0, 0)
        
        return fin_res[1] 

    def control(self, gameState, index, depth):
        if len(gameState.getLegalActions(index)) == 0 or gameState.isLose() or gameState.isWin() or depth == self.depth:
          return self.evaluationFunction(gameState), ""
          
        if index == 0:
          return self.max_act(gameState, index, depth)
        else:
          return self.exp_act(gameState, index, depth)


    def max_act(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)

        max_value = float("-inf")
        max_action = ""
          

        for action in moves:
          successor = gameState.generateSuccessor(index, action)
          new_index = index + 1
          new_depth = depth
          
          if new_index == gameState.getNumAgents():
            new_index = 0
            new_depth += 1

          min_agent = self.control(successor, new_index, new_depth)

          if min_agent[0] > max_value:
            max_value = min_agent[0]
            max_action = action

        return max_value, max_action

    def exp_act(self, gameState, index, depth):
        moves = gameState.getLegalActions(index)

        expected_value = 0
        expected_action = ""

        for action in moves:

          successor = gameState.generateSuccessor(index, action)
          new_index = index + 1
          new_depth = depth
          
          if new_index == gameState.getNumAgents():
            new_index = 0
            new_depth += 1

          max_agent = self.control(successor, new_index, new_depth)

          expected_value += float(max_agent[0])/len(moves)
        expected_action = max_agent[1]
        return expected_value, expected_action  
        #util.raiseNotDefined()
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      Evaluate state by  :
            * closest food
            * food left
            * capsules left
            * distance to ghost
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    oldGhostStates = currentGameState.getGhostStates()
    oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
    capsules = currentGameState.getCapsules()
    walls = currentGameState.getWalls()
    score = 0
    nearest_ghost = []
    for ghost in oldGhostStates:
      nearest_ghost += [manhattanDistance(ghost.configuration.pos, newPos)]

    NFood = newFood.asList()
    if len(NFood) == 0 :
      return currentGameState.getScore()

        #other_line = NFood[0]
    food = NFood[0]
    nearest_food = manhattanDistance(newPos, food)
    for f in NFood:
      temp = manhattanDistance(newPos, f)
      if temp < nearest_food:
        nearest_food = temp
        
    if len(capsules) != 0 :
      cap = capsules[0]
      nearest_capsule = manhattanDistance(newPos, cap)
      for c in capsules:
        temp = manhattanDistance(newPos, c)
        if temp < nearest_capsule:
          nearest_capsule = temp  

    
    nearest_wall = []
    for w in walls:
        nearest_wall+= [manhattanDistance(newPos, w)]

        
    i = len(NFood)
    for t in range(0, len(oldScaredTimes)):
      if oldScaredTimes[t] != 0:
        score += nearest_ghost[t]/(nearest_food)/(nearest_ghost[t]*500)
      else:
        if nearest_ghost[t] <= 1.0:
          score -= nearest_ghost[t]/999999
        else:
          if len(capsules) != 0:
            if nearest_capsule <= 3.0:
              score += nearest_capsule/999999
            else:
              score += nearest_ghost[t]/(nearest_food*50)
          else:
            score += nearest_ghost[t]/(nearest_food*50)
              

       
        
    return currentGameState.getScore() + score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction