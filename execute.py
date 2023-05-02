# Diese Datei wird ausgeführt
from castor.game import *

# Achtung: Beim Import wird direkt alles ausgeführt!
# import server_stuff.server as server
# import server_stuff.client as client

if __name__ == '__main__':
    # Das hier drunter wird nur dann beachtet, wenn die Datei selber ausgeführt wird.
    # Wenn man diese Datei importiert und dann versucht auszuführen, passiert nichts.

    game = Game()
    print(game.players)
    print(game.deck)
    game.deal_cards_to_all()
    print(game.players)
    print(game.deck)
    print(game)
    played_card = game.players[0].play_card_at_index(2)
    game.ablage.append(played_card)

    state = game.export_current_state()
    game.import_state(state)
    print(game.players[2].turn)
    print(game.deck[3].return_suit())
    print(game.ablage[0].return_value())
    print(game.start_cards, type(game.start_cards))
