from abc import ABC, abstractmethod

class Game:
    def __init__(self, args):
        self.initGameState(args)
        self.game_history = [self.game_state]
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)

    # MUST define game_state
    @abstractmethod
    def initGameState(self, args):
        self.game_state = None

    # DEFINE for saving each state to Game History
    @abstractmethod
    def copyAndSave(self):
        pass

    # SHOULD RETURN...
    #   0 -- if not a terminal state
    #   1 or 2 corresponding to the winning player if it is terminal
    #   3 corresponds to a tie
    @abstractmethod
    def isTerminalState(self):
        return 0

    # Updates the GameState to reflect the given action taken (mutates)
    @abstractmethod
    def takeAction(self, action):
        pass

    # Visualization method
    @abstractmethod
    def printGame(self):
        pass

    # main running method
    def run(self, debug=False):
        gameOver = False
        while not gameOver:
            for p in self.players:
                if not self.isTerminalState():
                    action = p.getNextAction(self)
                    while not action.isValidAction(self):
                        action = p.getNextAction(self)
                    self.copyAndSave()
                    self.takeAction(action)
                    if debug:
                        self.printGame()
                else:
                    gameOver = True

        print("Winner: %s" % self.players[self.isTerminalState() - 1])
                

class Action:
    def __init__(self, actor, args):
        self.actor = actor
        self.initAction(args)

    @abstractmethod
    def initAction(self, args):
        pass

    @abstractmethod
    def isValidAction(self):
        return True


class Agent:
    def __init__(self, id, args):
        self.id = id
        self.initAgent(args)

    def __str__(self):
        return "P%d" % self.id

    @abstractmethod
    def initAgent(self, args):
        pass

    @abstractmethod
    def getNextAction(self, game):
        pass

