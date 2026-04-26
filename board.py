import copy

class TTTGame:
    def __init__(self, state=[
        ["?", "?", "?"],
        ["?", "?", "?"],
        ["?", "?", "?"],
    ]):
        self.state = state

    @classmethod
    def next_player(cls, cur):
        if cur == "X":
            return "O"
        
        return "X"

    @classmethod
    def player(cls, board):
        xs = 0
        os = 0

        for row in board:
            for col in row:
                if col == "X":
                    xs += 1
                elif col == "O":
                    os += 1

        if xs > os:
            return "O"
        elif os > xs:
            return "X"
        else:
            return "X"
    
    def result(self, action):
        row = action[0]-1
        col = action[1]-1

        player = self.player(self.state)
        new = copy.deepcopy(self.state)

        if new[row][col] == "?":
            new[row][col] = player
        else:
            raise ValueError

        self.state = new

    def winner(self):
        board = self.state
        
        for row in board:
            if all(col == "X" for col in row):
                return "X"
            elif all(col == "O" for col in row):
                return "O"

        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] != "?":
                return board[0][i]

        if board[0][0] == board[1][1] == board[2][2] != "?":
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != "?":
            return board[0][2]

        return None

    @classmethod
    def available_actions(cls, board):
        empties = []

        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if col == "?":
                    empties.append((i+1, j+1))

        return empties

    def terminal(self):
        filled = 0
        
        for row in self.state:
            if "?" not in row:
                filled += 1

        if filled == 3:
            return True
        
        return False