from abc import ABC, abstractmethod

class Game(ABC):

    def __init__(self, players, initial_state):
        '''
        Turn order is implicit in the order of the list of
        players provided
        :param players:
        :param initial_state:
        '''
        self.players = players
        self.isDone = False
        self.State = initial_state

    def step(self):
        '''
        stops the game if there is winner and returns it
        '''
        for player in self.players:
            player.move(self)
            winner = self.victoryTest()
            if winner is not None:
                return winner

    @abstractmethod
    def advanceGameState(self, state):
        self.state = state

    @abstractmethod
    def getSuccessorStates(self, action):
        pass

    @abstractmethod
    def victoryTest(self):
        '''
        Based on the current state, returns the winner of the game if there is one or returns None
        '''
        pass

    def play(self):
        winner = None
        while not self.isDone and winner is not None:
            winner = self.step()