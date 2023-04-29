# Diese Datei wird ausgeführt
from castor.game import *

if __name__ == '__main__':
    # Das hier drunter wird nur dann beachtet, wenn die Datei selber ausgeführt wird.
    # Wenn man diese Datei importiert und dann versucht auszuführen, passiert nichts.

    game = Game()
    print(game.players)
    print(game.deck)
    game.deal_cards_to_all()
    print(game.players)
    print(game.deck)

    game.player_drops_card(game.get_current_player_num(), 0)
    print(game.ablage)
    print(game.get_current_player())
    print(game.check_top_card(Card(suit=1, value=1)))
