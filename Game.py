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
        for player in self.players:
            player.move(self)

    @abstractmethod
    def advanceGameState(self, state):
        self.state = state

    @abstractmethod
    def getSuccessorStates(self, action):
        pass

    def play(self):
        while not self.isDone:
            self.step()
