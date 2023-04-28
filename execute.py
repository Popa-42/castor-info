# Diese Datei wird ausgeführt
from castor.game import *

if __name__ == '__main__':
    # Das hier drunter wird nur dann beachtet, wenn die Datei selber ausgeführt wird.
    # Wenn man diese Datei importiert und dann versucht auszuführen, passiert nichts.

    # Erstelle ein Pik-Ass
    karte = Karte(1, 1)
    print(karte)

    deck = Deck()
    print(deck)
