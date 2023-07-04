import sys, os
sys.path.append(os.path.abspath(os.path.join('.', 'SolitaireLogic')))

from SolitaireLogic.cards import CardRenderer
from SolitaireLogic.deal_game import FreecellGame
from SolitaireLogic.random_base import RandomBase
fc24 = FreecellGame(
    game_num=24,
    which_deals=RandomBase.DEALS_MS
)
ms24_str = fc24.calc_layout_string(
    CardRenderer(print_ts=True)
)
print(fc24, end='')
print(fc24.board._lines)
