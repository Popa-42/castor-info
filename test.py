# Diese Datei wird ausgeführt
from castor.game import *

# Achtung: Beim Import wird direkt alles in den Dateien, was nicht unter 'if __name__ == "__main__"' steht, ausgeführt!
import server_stuff.server as server
import server_stuff.client as client

if __name__ == '__main__':
    # Das hier drunter wird nur dann beachtet, wenn die Datei selber ausgeführt wird.
    # Wenn man diese Datei importiert und dann versucht auszuführen, passiert nichts.

    game = Game(erster_spieler=3)
    print(game.spielerliste)
    print(game.deck)
    game.deal_cards_to_all()
    print(game.spielerliste)
    print(game.deck)
    print(game)
    played_card = game.spielerliste[0].play_card_at_index(2)
    game.ablage.append(played_card)

    state = game.export_current_state()
    game.import_state(state)
    print(game.spielerliste[2].hand[0].return_suit())
    print(game.deck[3].return_suit())
    print(game.ablage[0].return_value(), type(game.ablage[0].return_value()))
    print(game.anfangskarten, type(game.anfangskarten))
    print(game.game_over, type(game.game_over))
    print(game.aktueller_spieler, type(game.aktueller_spieler))
    game.next_player()
    print(game.aktueller_spieler)
