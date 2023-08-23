from enum import Enum

class ColumnType(Enum):
    COLUMN = 1
    FREECELL = 2
    FOUNDATION = 3

class MoveTypes(Enum):
    CToC = 1
    CToFC = 2
    CToF = 3
    
    FCToC = 4
    FCToFC = 5
    FCToF = 6
    
    FToC = 7
    FToFC = 8

class ValidMove(object):    
    def __init__(self, card, initColumn, initColumnType, endColumn, endColumnType):
        self.cardStack = card
        self.numOfCards = len(card)
        self.initColumn = initColumn
        self.initColumnType = initColumnType
        self.endColumn = endColumn
        self.endColumnType = endColumnType
        self.moveType = self.CreateMoveType(initColumnType, endColumnType)
        self.points = self.calculatePoints()
    
    def calculatePoints(self):
        return 1
    
    def CreateMoveType(self, initColumnType, endColumnType):
        if(initColumnType == ColumnType.COLUMN):
            if(endColumnType == ColumnType.COLUMN):
                return MoveTypes.CToC
            elif(endColumnType == ColumnType.FREECELL):
                return MoveTypes.CToFC
            elif(endColumnType == ColumnType.FOUNDATION):
                return MoveTypes.CToF
            
        elif(initColumnType == ColumnType.FREECELL):
            if(endColumnType == ColumnType.COLUMN):
                return MoveTypes.FCToC
            elif(endColumnType == ColumnType.FREECELL):
                return MoveTypes.FCToFC
            elif(endColumnType == ColumnType.FOUNDATION):
                return MoveTypes.FCToF
            
        elif(initColumnType == ColumnType.FOUNDATION):
            if(endColumnType == ColumnType.COLUMN):
                return MoveTypes.FToC
            elif(endColumnType == ColumnType.FREECELL):
                return MoveTypes.FToFC        

class ValidateMoves(object):
    def __init__(self, board):
        self.validMoveList = []
        self.board = board
        self.CreateValidMoves()
    
    def CheckWin(self):
        return self.board.foundations[0][0].rank == 13 and self.board.foundations[1][0].rank == 13 and self.board.foundations[2][0].rank == 13 and self.board.foundations[3][0].rank == 13

    def MoveCards(self, moveIndex):
        move = self.validMoveList[moveIndex]
        move.initColumn.remove(move.cardStack)
        move.endColumn.append(move.cardStack)
        self.CreateValidMoves()
        
    def CheckBoardForValidMove(self, column, columnType, card):
        if card.empty:
            return
        
        for newColumn in self.board.columns:
            newCard = newColumn[-1]
            if(self.valid_column_fc_moves(card, newCard)):
                print("Column Move: ", columnType, " ", card.rank, card.suit_s(), " to Column-", self.board.columns.index(newColumn), " ", newCard.rank, newCard.suit_s())
                self.validMoveList.append(ValidMove(column[:column.index(card)], column, columnType, newColumn ,ColumnType.COLUMN))
        for freecell in self.board.freecells:
            newCard = freecell[-1]
            if(self.valid_column_fc_moves(card, newCard)):
                print("Freecell Move: ", columnType, " ", card.rank, card.suit_s(), " to Freecell-", self.board.freecells.index(freecell), " ", newCard.rank, newCard.suit_s())
                self.validMoveList.append(ValidMove(column[:column.index(card)], column, columnType, freecell, ColumnType.FREECELL))
        for foundation in self.board.foundations:
            newCard = foundation[-1]
            if(self.valid_foundation_moves(self.board.foundations.index(foundation), card, newCard)):
                print("Foundation Move: ", columnType, " ", card.rank, card.suit_s(), " to Foundation-", 'CSHD'[self.board.foundations.index(foundation)], " ", newCard.rank, newCard.suit_s())
                self.validMoveList.append(ValidMove(column[:column.index(card)], column, columnType, foundation, ColumnType.FOUNDATION))

    def CreateValidMoves(self):
        for column in self.board.columns:
            column = list(reversed(column))
            cardIndex = 0
            if column:
                for card in column:
                    self.CheckBoardForValidMove(column, ColumnType.COLUMN, card)
                    if( not (column[cardIndex + 1] and self.check_stack(column, cardIndex, card))  ):
                        break
                    cardIndex = cardIndex + 1
        for freecell in self.board.freecells:
            freecell = list(reversed(freecell))
            if freecell:
                for card in freecell:
                    self.CheckBoardForValidMove(freecell, ColumnType.FREECELL, card)
        for foundation in self.board.foundations:
            foundation = list(reversed(foundation))
            if foundation:
                for card in foundation:
                    self.CheckBoardForValidMove(foundation, ColumnType.FOUNDATION, card)                   
                        
    def check_alternating_suits(self, startCard, endCard):
        return ( startCard.is_black() and  endCard.is_red() ) or ( startCard.is_red() and endCard.is_black() )
        
    def valid_column_fc_moves(self, startCard, endCard):
        if endCard.empty:
            return True
        return startCard.rank + 1 == endCard.rank and self.check_alternating_suits(startCard, endCard)
    
    def valid_foundation_moves(self, foundationSuit, startCard, endCard):
        if endCard.empty and startCard.rank == 1 and startCard.suit == foundationSuit:
            return True
        return startCard.rank + 1 == endCard.rank and startCard.suit == endCard.suit
    
    def check_stack(self, column, cardIndex, card):
        parentCard = column[cardIndex+1]
        return card.rank + 1 == parentCard.rank and self.check_alternating_suits(card, parentCard)
                
        
