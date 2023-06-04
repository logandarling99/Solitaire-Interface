import sys, os
sys.path.append(os.path.abspath(os.path.join('.', 'SolitaireLogic')))

from SolitaireLogic.cards import CardRenderer
from SolitaireLogic.deal_game import Game
from SolitaireLogic.random_base import RandomBase
ms24_str = Game(
    game_id="freecell",
    game_num=24,
    which_deals=RandomBase.DEALS_MS,
    max_rank=13
).calc_layout_string(
    CardRenderer(print_ts=True)
)
print(ms24_str, end='')