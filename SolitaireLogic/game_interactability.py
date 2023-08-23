from .game_moves import ValidateMoves

class Interactions(object):
    def __init__(self, board):
        self.board = board
        self.moveValidator = ValidateMoves(self.board)
        self.moves = self.validMoveList
    
    def MoveCards(self, moveIndex):
        move = self.moves[moveIndex]
        move.initColumn.remove(move.cardStack)
        move.endColumn.append(move.cardStack)
        self.moveValidator.CreateValidMoves()