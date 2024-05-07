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
from pacman import GameState

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.getPacmanNextState(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #  distancia promedio a los alimentos restantes
        dist2food = 0

        for food in newFood.asList():
            dist2food += manhattanDistance(food, newPos)

        if len(newFood.asList()) != 0:
            dist2food /= len(newFood.asList()) 

        # distancia promedio a los fantasmas
        dist2ghost = 0

        for ghostState in newGhostStates:
            dist2ghost += manhattanDistance(ghostState.getPosition(), newPos)

        if len(newGhostStates) != 0:
            dist2ghost /= len(newGhostStates) 

        # tiempo promedio restante para que los fantasmas dejen de estar asustados
        time2notscared = 0

        for scaredTime in newScaredTimes:
            time2notscared += scaredTime

        if len(newScaredTimes) != 0:
            time2notscared /= len(newScaredTimes) 
            
        return (successorGameState.getScore() * 4) - (dist2food * 1.25) + (time2notscared * 3) + (dist2ghost)


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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)

        actionValues = [self.getValue(gameState.getNextState(0, action), self.depth, 1) for action in actions]

        maxIndex = actionValues.index(max(actionValues))

        return actions[maxIndex]

    def getValue(self, gameState, depth, agentIndex):
        if depth == 0:  # if terminal state
            returnVal = self.evaluationFunction(gameState)
            return returnVal

        if gameState.isWin():
            returnVal = self.evaluationFunction(gameState)
            return returnVal

        if gameState.isLose():
            returnVal = self.evaluationFunction(gameState)
            return returnVal

        if (gameState.getNumAgents() == agentIndex + 1) and (depth > 0):  # last agent move for the current depth
            depth -= 1
        if agentIndex >= 1:  # min agent (ghost)
            return self.minValue(gameState, depth, agentIndex)
        if agentIndex == 0:  # max agent (pacman)
            return self.maxValue(gameState, depth, agentIndex)

    def minValue(self, gameState, depth, agentIndex):
        actions = gameState.getLegalActions(agentIndex)
        minVal = 9999
        for action in actions:
            successor = gameState.getNextState(agentIndex, action)
            minVal = min(minVal, self.getValue(successor, depth, (agentIndex + 1) % gameState.getNumAgents()))
        return minVal

    def maxValue(self, gameState, depth, agentIndex):

        actions = gameState.getLegalActions(agentIndex)
        maxVal = -9999

        for action in actions:
            successor = gameState.getNextState(agentIndex, action)
            maxVal = max(maxVal, self.getValue(successor, depth, (agentIndex + 1) % gameState.getNumAgents()))

        return maxVal

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)

        alpha = -9999
        beta = 9999

        maxVal = alpha

        actionToReturn = actions[0]

        for action in actions:
            successor = gameState.getNextState(0, action)
            maxVal = max(maxVal, self.getValue(successor, self.depth, 1, alpha, beta))

            if maxVal > beta:
                return action

            if maxVal > alpha:
                actionToReturn = action
                alpha = maxVal

        return actionToReturn
    
    def getValue(self, gameState, depth, agentIndex, alpha, beta):
        if depth == 0:  # if terminal state
            returnVal = self.evaluationFunction(gameState)
            return returnVal
        if gameState.isWin():
            returnVal = self.evaluationFunction(gameState)
            return returnVal
        if gameState.isLose():
            returnVal = self.evaluationFunction(gameState)
            return returnVal
        if (gameState.getNumAgents() == agentIndex + 1) and (depth > 0):  # last agent move for the current depth
            depth -= 1
        if agentIndex >= 1:  # min agent (ghost)
            return self.minValue(gameState, depth, agentIndex, alpha, beta)
        if agentIndex == 0:  # max agent (pacman)
            return self.maxValue(gameState, depth, agentIndex, alpha, beta)

    def minValue(self, gameState, depth, agentIndex, alpha, beta):

        actions = gameState.getLegalActions(agentIndex)

        minVal = 9999

        for action in actions:

            successor = gameState.getNextState(agentIndex, action)
            minVal = min(minVal,
                         self.getValue(successor, depth, (agentIndex + 1) % gameState.getNumAgents(), alpha, beta))

            if minVal < alpha:
                return minVal
            beta = min(beta, minVal)
        return minVal

    def maxValue(self, gameState, depth, agentIndex, alpha, beta):

        actions = gameState.getLegalActions(agentIndex)
        maxVal = -9999

        for action in actions:
            successor = gameState.getNextState(agentIndex, action)
            maxVal = max(maxVal,
                         self.getValue(successor, depth, (agentIndex + 1) % gameState.getNumAgents(), alpha, beta))
            if maxVal > beta:
                return maxVal
            alpha = max(alpha, maxVal)
        return maxVal

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Agente de Expectimax para el juego Pac-Man. El agente Expectimax modela a los oponentes (fantasmas)
    como si hicieran elecciones aleatorias entre sus movimientos legales, en lugar de jugar óptimamente.
    """

    def getAction(self, gameState):
        """
        Devuelve la acción de Expectimax usando la profundidad de búsqueda definida y la función de evaluación.

        :param gameState: El estado actual del juego.
        :return: La mejor acción según el algoritmo Expectimax.
        """
        # Obtener todas las acciones legales para Pac-Man (agente 0).
        actions = gameState.getLegalActions(0)

        # Calcular el valor de cada acción posible.
        actionValues = [self.getValue(gameState.getNextState(0, action), self.depth, 1) for action in actions]

        # Seleccionar el índice de la acción con el valor máximo.
        maxIndex = actionValues.index(max(actionValues))

        # Devolver la acción con el máximo valor.
        return actions[maxIndex]
    
    def getValue(self, gameState, depth, agentIndex):
        """
        Calcula el valor del estado dado, considerando la profundidad y el agente actual.

        :param gameState: Estado actual del juego.
        :param depth: Profundidad actual de la búsqueda.
        :param agentIndex: Índice del agente actual.
        :return: Valor calculado para el estado dado.
        """
        # Verificar si el estado es terminal por profundidad, victoria o derrota.
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Ajustar la profundidad si es el último agente.
        if gameState.getNumAgents() == agentIndex + 1:
            depth -= 1

        # Evaluar basándose en si el agente es Pac-Man o un fantasma.
        if agentIndex >= 1:
            # Valor esperado para los fantasmas.
            return self.expectedValue(gameState, depth, agentIndex)
        else:
            # Valor máximo para Pac-Man.
            return self.maxValue(gameState, depth, agentIndex)

    def maxValue(self, gameState, depth, agentIndex):
        """
        Calcula el valor máximo para las acciones de Pac-Man.

        :param gameState: Estado del juego.
        :param depth: Profundidad de búsqueda.
        :param agentIndex: Índice del agente.
        :return: El valor máximo.
        """
        # Obtener las acciones legales para Pac-Man.
        actions = gameState.getLegalActions(agentIndex)
        maxVal = float('-inf')  # Iniciar con un valor muy bajo.

        # Evaluar el valor máximo entre las acciones posibles.
        for action in actions:
            successor = gameState.getNextState(agentIndex, action)
            maxVal = max(maxVal, self.getValue(successor, depth, (agentIndex + 1) % gameState.getNumAgents()))
        return maxVal

    def expectedValue(self, gameState, depth, agentIndex):
        """
        Calcula el valor esperado para las acciones de un fantasma.

        :param gameState: Estado del juego.
        :param depth: Profundidad de búsqueda.
        :param agentIndex: Índice del fantasma.
        :return: Valor esperado.
        """
        # Obtener acciones legales para el fantasma.
        actions = gameState.getLegalActions(agentIndex)
        valSum = 0  # Suma de valores para calcular la media.

        # Sumar los valores de todas las acciones posibles.
        for action in actions:
            successor = gameState.getNextState(agentIndex, action)
            val = self.getValue(successor, depth, (agentIndex + 1) % gameState.getNumAgents())
            valSum += val

        # Calcular el promedio si hay acciones disponibles.
        return valSum / len(actions) if actions else 0
    
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
