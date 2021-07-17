"""
file responsible storing all the information about the current state of a chess game.
"""

class GameState():
    def __init__(self):
        #board is a 8x8 2d list of 1 characters elements.
        #lower case is black uppercase is white
        #each character represent one piece
        self.board = [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","P","p","p","p","p"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["P","P","P","P","p","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'r': self.getRookMove, 'n': self.getKnightMove,
                              'b': self.getBishipMove, 'q': self.getQueenMove, 'k': self.getKingMove }
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        """
        takes a move and execute it.(does not work for casteling,paw promotion , and en-passant)

        Args:
            move (Move): Move class object
        """
        self.board[move.startRow][move.startCol] = "."
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        '''
        Unduo last move
        '''
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove


    '''
    All moves considering checks
    '''
    def getValidMoves(self): # TODO: consider checks
        return self.getAllPossibleMoves()
    '''
    All possible moves
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if(piece.isupper() and self.whiteToMove) or (piece.islower() and not self.whiteToMove):
                    self.moveFunctions[piece.lower()](r, c, moves)
        return moves


    '''
    Get all the pawn moves for the pawn located at row, col and add to the move list
    '''
    #FIXME:pawn in the last sq brakes the function
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn
            if self.board[r-1][c] == '.':
                moves.append(Move(( r, c),(r-1, c), self.board))
                if r==6 and self.board[r-2][c] == '.':
                    moves.append(Move((r, c), (r-2,c), self.board))
            if c-1>=0:
                if self.board[r-1][c-1].islower():
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7:
                if self.board[r-1][c+1].islower():
                    moves.append(Move((r,c),(r-1,c+1),self.board))

        if not self.whiteToMove:#black pawn
            if self.board[r+1][c] == '.':
                moves.append(Move(( r, c),(r+1, c), self.board))
                if r==1 and self.board[r+2][c] == '.':
                    moves.append(Move((r, c), (r+2,c), self.board))
            if c-1>=0:
                if self.board[r+1][c-1].isupper():
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7:
                if self.board[r+1][c+1].isupper():
                    moves.append(Move((r,c),(r+1,c+1),self.board))

    '''
    Get all the Rook moves for the Rook located at row, col and add to the move list
    '''
    def getRookMove(self, r, c, moves):
        pass

    '''
    Get all the Knight moves for the Knight located at row, col and add to the move list
    '''
    def getKnightMove(self, r, c, moves):
        pass

    '''
    Get all the Biship moves for the Biship located at row, col and add to the move list
    '''
    def getBishipMove(self, r, c, moves):
        pass

    '''
    Get all the Queen moves for the Queen located at row, col and add to the move list
    '''
    def getQueenMove(self, r, c, moves):
        pass

    '''
    Get all the King moves for the King located at row, col and add to the move list
    '''
    def getKingMove(self, r, c, moves):
        pass


class Move():
    #maps keys to values
    #key :value
    ranksToRows = {"1": 7, "2": 6, "2": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self,startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #cria um id unico para o posicao inicial e posicao final da forma RiCiRfCf
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    overriding the equals method
    TODO: nao precisaria ser usado se nao estivesse usando a classe Move e no lugar fosse uma string
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self, r , c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
