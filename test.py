# Diese Datei wird ausgeführt
from castor.game import *

if __name__ == '__main__':
    # Das hier drunter wird nur dann beachtet, wenn die Datei selber ausgeführt wird.
    # Wenn man diese Datei importiert und dann versucht auszuführen, passiert nichts.

    # Initialisiere ein neues Spiel
    game = Game(erster_spieler=3)
    print(game.players)
    print(game.deck)
    game.deal_cards_to_all()
    print(game.players)
    print(game.deck)
    print(game)
    played_card = game.players[0].play_card_at_index(2)
    game.ablage.append(played_card)

    # Funktioniert Export / Import?
    state = game.export_current_state()
    game.import_state(state)
    print(game.players[2].hand[0].suit_str())
    print(game.deck[3].suit_str())
    print(game.ablage[0].value_str(), type(game.ablage[0].value_str()))
    print(game.anfangskarten, type(game.anfangskarten))
    print(game.game_over, type(game.game_over))
    print(game.current_player, type(game.current_player))
    game.next_player()
    print(game.current_player)
