from GeneralGame import Game, Action, Agent
import random 

class Othello(Game):

    def initGameState(self, args):
        self.N = args['N']
        # 0 represents no element, 1 is P1, 2 is P2
        self.game_state = self.N * [self.N * [0]]

    def copyAndSave(self):
        self.game_history.append(self.game_state)
        self.game_state = [[self.game_state[i][j] for j in range(self.N)] for i in range(self.N)] 

    def isTerminalState(self):
        cnt1 = 0
        cnt2 = 0
        for i in range(self.N):
            for j in range(self.N):
                piece = self.game_state[i][j] 
                if piece == 0:
                    return 0
                elif piece == 1:
                    cnt1 += 1
                elif piece == 2:
                    cnt2 += 1
                else:
                    return 'ERROR IN GAME_STATE TYPE'

        if cnt1 > cnt2:
            return 1
        elif cnt2 > cnt1:
            return 2
        else:
            return 3

    #helper
    def propogate_point(self, val, func, initialPoint):
        currpt = func(initialPoint[0], initialPoint[1])
        found = False
        while 0 <= currpt[0] < self.N and 0 <= currpt[1] < self.N:
            if self.game_state[currpt[0]][currpt[1]] == val:
                found = True
            elif self.game_state[currpt[0]][currpt[1]] == 0:
                break
            currpt = func(currpt[0], currpt[1])

        #if there is no terminating piece, don't do anything
        if not found:
            return

        #set all the pieces on that path to the right color
        currpt = func(initialPoint[0], initialPoint[1])
        while self.game_state[currpt[0]][currpt[1]] != val:
            self.game_state[currpt[0]][currpt[1]] = val
            currpt = func(currpt[0], currpt[1])


    def takeAction(self, action):
        self.game_state[action.row][action.col] = action.newVal
        #UP 
        self.propogate_point(action.newVal, lambda r,c : (r-1,c), (action.row, action.col))
        #UP LEFT
        self.propogate_point(action.newVal, lambda r,c : (r-1,c-1), (action.row, action.col))
        #LEFT
        self.propogate_point(action.newVal, lambda r,c : (r,c-1), (action.row, action.col))
        #DOWN LEFT
        self.propogate_point(action.newVal, lambda r,c : (r+1,c-1), (action.row, action.col))
        #DOWN 
        self.propogate_point(action.newVal, lambda r,c : (r+1,c), (action.row, action.col))
        #DOWN RIGHT
        self.propogate_point(action.newVal, lambda r,c : (r+1,c+1), (action.row, action.col))
        #RIGHT
        self.propogate_point(action.newVal, lambda r,c : (r,c+1), (action.row, action.col))
        # UP RIGHT
        self.propogate_point(action.newVal, lambda r,c : (r-1,c+1), (action.row, action.col))

    def printGame(self):
        for i in range(self.N):
            print(" ---" * self.N)
            row = "|" + " %d |" * self.N
            print(row % tuple(self.game_state[i]))

        print(" ---" * self.N)


class OthelloAction(Action):

    def initAction(self, args):
        self.row, self.col = args['ROW'], args['COL']
        self.newVal = args['PLAYER']

    def isValidAction(self, game):
        inRange = self.row < game.N and self.col < game.N and self.row >= 0 and self.col >= 0
        valid = self.newVal == 1 or self.newVal == 2
        return valid and inRange


class RandomOthelloAgent(Agent):

    def initAgent(self, args):
        pass

    #just picks a random action
    def getNextAction(self, game):
        if not isinstance(game, Othello):
            raise Exception("This agent is meant for Othello!")
        else:
            #count empty spots
            lst = []
            for i in range(game.N):
                for j in range(game.N):
                    if game.game_state[i][j] == 0:
                        lst.append((i,j))

            if len(lst) > 0:
                pnt = lst[random.randint(0, len(lst)-1)]
                return OthelloAction(self, {'ROW':pnt[0], 'COL':pnt[1], 'PLAYER':self.id})


if __name__ == "__main__":
    game = Othello({'N':5})
    p1 = RandomOthelloAgent(1, None)
    p2 = RandomOthelloAgent(2, None)
    game.addPlayer(p1)
    game.addPlayer(p2)
    game.run(debug=True)