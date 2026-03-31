# pylint: disable=too-few-public-methods
# multiAgents.py (original)
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
        score = successorGameState.getScore()

        foodlist = newFood.asList()
        if len(foodlist) == 0 :
          return successorGameState.getScore()

        food = foodlist[0]
        nearest_food_pos = manhattanDistance(newPos, food)
        for f in foodlist:
          temp = manhattanDistance(newPos, f)
          if temp < nearest_food_pos:
            nearest_food_pos = temp    
        
        if action == 'Stop':
            score -= 10

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

          gameState.getLegalActions(index):
            Returns a list of legal actions for an agent
            index=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(index, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        def minimax(index, depth, gamestate):
              #check for end or max depth
              if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                  return self.evaluationFunction(gamestate)
              # max agent pacman
              if index == 0: return maxValue(index, depth, gamestate)
              #min agents ghosts
              else: return minValue(index, depth, gamestate)

        def maxValue(index, depth, gamestate):
            v = float('-inf')
            legalactions = gamestate.getLegalActions(index)
            for action in legalactions:
                successor = gamestate.generateSuccessor(index, action)
                v = max(v, minimax(1, depth, successor))  #agent 1
            return v

        def minValue(index, depth, gamestate):
            v = float('inf')
            legalActions = gamestate.getLegalActions(index)
            nextagent = index + 1
            numagents = gameState.getNumAgents()

            for action in legalActions:
                successor = gamestate.generateSuccessor(index, action)
                #if last ghost go to max agent
                if nextagent == numagents:  v = min(v, minimax(0, depth + 1, successor))
                else: v = min(v, minimax(nextagent, depth, successor))
            return v

        legalactions = gameState.getLegalActions(0)
        result = None
        bestvalue = float('-inf')

        for action in legalactions:
            successor = gameState.generateSuccessor(0, action)
            value = minimax(1, 0, successor)  #ghost 1
            if value > bestvalue:
                bestvalue = value
                result = action

        return result
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def alphaBeta(gamestate, depth, alpha, beta, index):
            if index == 0: return maxValue(gamestate, depth, alpha, beta, index)
            else:  return minValue(gamestate, depth, alpha, beta, index)

        def maxValue(gamestate, depth, alpha, beta, index):
            value = float('-inf')
            legalactions = gamestate.getLegalActions(index)
            
            if not legalactions or depth == self.depth:
                return self.evaluationFunction(gamestate)
            
            for action in legalactions:
                successor = gamestate.generateSuccessor(index, action)
                value = max(value, alphaBeta(successor, depth, alpha, beta, index + 1))
                if value > beta:  return value  #prune
                alpha = max(alpha, value)
            return value

        def minValue(gamestate, depth, alpha, beta, index):
            value = float('inf')
            legalactions = gamestate.getLegalActions(index)
            
            if not legalactions: return self.evaluationFunction(gamestate)
            
            numagents = gameState.getNumAgents()
            nextagent = (index + 1) % numagents
            
            for action in legalactions:
                successor = gamestate.generateSuccessor(index, action)
                if nextagent == 0: value = min(value, alphaBeta(successor, depth + 1, alpha, beta, nextagent)) #if next is pacman inc depth
                else: value = min(value, alphaBeta(successor, depth, alpha, beta, nextagent))
                if value < alpha: return value
                beta = min(beta, value)
            return value

        alpha = float('-inf')
        beta = float('inf')
        result = None
        bestscore = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = alphaBeta(successor, 0, alpha, beta, 1)
            if value > bestscore:
                bestscore = value
                result = action
            alpha = max(alpha, bestscore)

        return result


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction.
        All ghosts should be modeled as choosing uniformly at random from their legal moves.
        """
        def expectimax(gamestate, depth, index):
            if index == 0: return maxValue(gamestate, depth, index)
            else: return expectedValue(gamestate, depth, index)

        def maxValue(gamestate, depth, index):
            v = float('-inf')
            legalactions = gamestate.getLegalActions(index)

            if not legalactions or depth == self.depth:
                return self.evaluationFunction(gamestate)

            for action in legalactions:
                successor = gamestate.generateSuccessor(index, action)
                v = max(v, expectimax(successor, depth, index + 1))

            return v

        def expectedValue(gamestate, depth, index):
            legalactions = gamestate.getLegalActions(index)
            if not legalactions:
                return self.evaluationFunction(gamestate)
            
            actions = len(legalactions)
            totalvalue = 0

            for action in legalactions:
                successor = gamestate.generateSuccessor(index, action)
                nextagent = (index + 1) % gamestate.getNumAgents()
                if nextagent == 0:  totalvalue += expectimax(successor, depth + 1, nextagent) # pac move inc depth
                else: totalvalue += expectimax(successor, depth, nextagent)

            return totalvalue / actions  # average

        result = None
        bestscore = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = expectimax(successor, 0, 1)
            if value > bestscore:
                bestscore = value
                result = action

        return result

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:  +score : close scared ghost, go to food
                    -score : close to ghost, much food remaining, many ghosts active and stop moving
    """
    pacmanpos = currentGameState.getPacmanPosition()
    foodpos = currentGameState.getFood()
    ghoststates = currentGameState.getGhostStates()
    scaredtimes = []
    for ghoststate in ghoststates:
        scaredtimes.append(ghoststate.scaredTimer)

    score = currentGameState.getScore()

    foodlist = foodpos.asList()
    if foodlist:
        closestfood = min(manhattanDistance(pacmanpos, food) for food in foodlist)
        score += 10.0 / (closestfood + 1)  #go to food

    # -score if ghost close +score if close to scared ghost
    for ghoststate, scaredtime in zip(ghoststates, scaredtimes):
        ghostpos = ghoststate.getPosition()
        ghostdist = manhattanDistance(pacmanpos, ghostpos)

        if scaredtime > 0:
            score += 20.0 / (ghostdist + 1)  #pac to ghosts if scared
        elif ghostdist < 2:
            score -= 100.0

    foodtoeat = len(foodlist)
    score -= foodtoeat * 2  #reduce for more food

    ghosts = len(ghoststates)
    scared = 0
    for time in scaredtimes:
        if time > 0:
            scared += 1
    active = ghosts - scared

    if scared > 0:
        score += scared * 50  #bonus for scared ghost

    if active > 0:
        score -= active * 10 #-score if many ghosts active

    if currentGameState.getPacmanPosition() == pacmanpos:
        score -= 10

    return score

# Abbreviation
better = betterEvaluationFunction


  