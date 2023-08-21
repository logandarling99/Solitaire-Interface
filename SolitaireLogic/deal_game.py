# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under terms of the Expat license.

"""

"""

from .cards import Card, createCards
from .solrandom import shuffle
import traceback

from six import print_

def empty_card():
    ret = Card(-1, 0, 0)
    ret.empty = True
    return ret

class Board(object):
    def __init__(self):
        self.columns = [[] for _ in range(8)]
        self.freecells = [[empty_card()] for _ in range(4)]
        self.foundations = [[empty_card()] for _ in range(4)]
        self._lines = []            
    
    def add_line(self, string):
        self._lines.append(string)
    
    def add(self, idx, card):
        self.columns[idx].append(card)
    
    def translateIndexToColumn(self, index):
        if(index < 8):
            return self.columns[index]
        elif(index < 12):
            return self.freecells[index-8]
        elif(index < 16):
            return self.foundations[index-12]
            
    def moveCards(self, startIndex, moveIndex, card):
        initIdxList = self.translateIndexToColumn(startIndex)
        cardListIdx = initIdxList.index(card)
        newColumnList = self.translateIndexToColumn(moveIndex)
        cardList = initIdxList[cardListIdx:]
        newColumnList.append(cardList)
        
    def print_foundations(self, renderer):
        cells = []
        for f in range(4):
            for card in self.foundations[f]:
                if not card.empty:
                    cells.append(renderer.found_s(card))
            
        if len(cells):
            self.add_line("Foundations:" + ("".join([" " + s for s in cells])))
    
    def gen_lines(self, renderer):
        self._lines = []
        self.print_foundations(renderer)
        #self.add_line("Freecells: " + renderer.l_concat(self.freecells))
        self._lines += [renderer.l_concat(c) for c in self.columns]
    
    def calc_string(self, renderer):
        self.gen_lines(renderer)
        return "".join(l + "\n" for l in self._lines)

class FreecellGame(object):
    
    def __init__(self, game_num, which_deals, max_rank=13):
        self.game_num = game_num
        self.which_deals = which_deals
        self.max_rank = max_rank
    
    def calc_deal_string(self, game_num, renderer):
        self.game_num = game_num
        self.deal()
        getattr(self, "freecell")()
        return self.board.calc_string(renderer)
    
    def calc_layout_string(self, renderer):
        self.deal()
        getattr(self, "freecell")()
        return self.board.calc_string(renderer)
    
    def print_layout(self, renderer):
        print_(self.calc_layout_string(renderer), sep='', end='')
    
    def new_cards(self, cards):
        self.cards = cards
        self.card_idx = 0
    
    def deal(self):
        cards = shuffle(createCards(self.max_rank), self.game_num, self.which_deals)
        cards.reverse()
        self.new_cards(cards)
    
    def __iter__(self):
        return self
    
    def no_more_cards(self):
        return self.card_idx >= len(self.cards)
    
    def __next__(self):
        if self.no_more_cards():
            raise StopIteration
        c = self.cards[self.card_idx]
        self.card_idx += 1
        return c
    
    def next(self):
        return self.__next__()
    
    def add(self, idx, card):
        self.board.add(idx, card)
    
    def cyclical_deal(self, num_cards, num_cols, flipped=False):
        for i in range(num_cards):
            self.add(i % num_cols, next(self).flip(flipped=flipped))
    
    def freecell(game):
        game.board = Board()
        max_rank = game.max_rank
        game.cyclical_deal(4 * max_rank, 8)
