from flask import Flask
from flask_cors import CORS
from flask import request

from imagedetect import *

app = Flask(__name__)
CORS(app)

class Validate:
    def isValidSudoku(self, board):
        return (self.is_row_valid(board) and self.is_col_valid(board) and self.is_square_valid(board))

    def is_row_valid(self, board):
        for row in board:
            if not self.is_unit_valid(row):
                return False
        return True

    def is_col_valid(self, board):
        for col in zip(*board):
            if not self.is_unit_valid(col):
                return False
        return True
        
    def is_square_valid(self, board):
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if not self.is_unit_valid(square):
                    return False
        return True
        
    def is_unit_valid(self, unit):
        unit = [i for i in unit if i != '-']
        return len(set(unit)) == len(unit)

class Solve:
    def solveSudoku(self, board):
        self.board = board
        self.solve()
        return self.board
    
    def findUnassigned(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == "-":
                    return row, col
        return -1, -1
    
    def solve(self):
        row, col = self.findUnassigned()
        if row == -1 and col == -1:
            return True
        for num in ["1","2","3","4","5","6","7","8","9"]:
            if self.isSafe(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = "-"
        return False
            
    def isSafe(self, row, col, ch):
        boxrow = row - row%3
        boxcol = col - col%3
        if self.checkrow(row,ch) and self.checkcol(col,ch) and self.checksquare(boxrow, boxcol, ch):
            return True
        return False
    
    def checkrow(self, row, ch):
        for col in range(9):
            if self.board[row][col] == ch:
                return False
        return True
    
    def checkcol(self, col, ch):
        for row in range(9):
            if self.board[row][col] == ch:
                return False
        return True
       
    def checksquare(self, row, col, ch):
        for r in range(row, row+3):
            for c in range(col, col+3):
                if self.board[r][c] == ch:
                    return False
        return True

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.files:
            image = cv2.imdecode(np.fromstring(request.files['myfile'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
            return {"result": extract_board(image)}
        else:
            lst = list(request.data.decode('utf-8').replace('[', '').replace(']', '').replace('"', '').replace(',',''))
            board = []
            tmp = []
            for i in range(len(lst)):
                if i != 0 and i % 9 == 0:
                    board.append(tmp)
                    tmp = []
                tmp.append(lst[i])
            board.append(tmp)
            checkValidity = Validate()
            if(checkValidity.isValidSudoku(board) == False):
                return {"result": "INVALID"}
            else:
                solveBoard = Solve()
                return {"result": solveBoard.solveSudoku(board)}
    elif request.method == 'GET':
        return "<h1>Hello World</h1>"

if __name__ == '__main__':
    app.run(debug=True)