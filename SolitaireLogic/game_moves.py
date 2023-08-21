from .deal_game import FreecellGame
from .random_base import RandomBase
from .cards import CardRenderer

fc24 = FreecellGame(
    game_num=24,
    which_deals=RandomBase.DEALS_MS
)

ms24_str = fc24.calc_layout_string(
    CardRenderer(print_ts=True)
)

class ValidateMoves():
    def __init__(self):
        self.validMoveList = []
        
    def checkBoardForValidMove(self, card):
        for newColumn in fc24.board.columns:
            newCard = newColumn[-1]
            if(self.valid_column_fc_moves(card, newCard)):
                print("Column Move: ", card.rank, card.suit_s(), " to Column-", fc24.board.columns.index(newColumn), " ", newCard.rank, newCard.suit_s())
        for freecell in fc24.board.freecells:
            newCard = freecell[-1]
            if(self.valid_column_fc_moves(card, newCard)):
                print("Freecell Move: ", card.rank, card.suit_s(), " to Freecell-", fc24.board.freecells.index(freecell), " ", newCard.rank, newCard.suit_s())
        for foundation in fc24.board.foundations:
            newCard = foundation[-1]
            if(self.valid_foundation_moves(fc24.board.foundations.index(foundation), card, newCard)):
                print("Foundation Move: ", card.rank, card.suit_s(), " to Foundation-", 'CSHD'[fc24.board.foundations.index(foundation)], " ", newCard.rank, newCard.suit_s())
    
    def createValidMoves(self):
        for column in fc24.board.columns:
            column = list(reversed(column))
            cardIndex = 0
            if column:
                for card in column:
                    self.checkBoardForValidMove(card)
                    if( not (column[cardIndex + 1] and self.check_stack(column, cardIndex, card))  ):
                        break
                    cardIndex = cardIndex + 1
        for freecell in fc24.board.freecells:
            freecell = list(reversed(freecell))
            if freecell:
                for card in freecell:
                    self.checkBoardForValidMove(card)
        for foundation in fc24.board.foundations:
            foundation = list(reversed(foundation))
            if foundation:
                for card in foundation:
                    self.checkBoardForValidMove(card)                   
                        
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
            
    
    
        
        
