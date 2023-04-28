# Das Backend für Castor
# → Das grundlegende Kartenspiel

from random import shuffle


class Karte:
    def __init__(self,
                 suit: int | None,
                 value: int):
        """
        Eine Spielkarte mit Farbe und Wert.

        :param suit: Die Farbe der Karte
        :param value: Der Wert der Karte
        """
        self.suit = suit
        self.value = value

    def __repr__(self) -> str:
        """
        Was bei ``str(Karte)`` bzw ``print(Karte)`` zurückgegeben wird, z.B.:

        >>> karte = Karte(suit=1, value=1)
        >>> print(karte)
        'Karte(suit=1, value=1)'

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Eine String-Repräsentation des Objekts
        """
        return f"{self.__class__.__name__}(suit={self.suit}, value={self.value})"

    def return_suit(self) -> str:
        """
        Gibt die Farbe der jeweiligen Karte in Form eines Strings zurück.

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Die Farbe der Karte
        """
        if self.suit == 0:
            return "Kreuz"
        if self.suit == 1:
            return "Pik"
        if self.suit == 2:
            return "Herz"
        if self.suit == 3:
            return "Karo"
        if not self.suit:
            return ""
        raise IndexError("Diese Farbe existiert nicht.")

    def return_value(self) -> str:
        """
        Gibt den Wert der jeweiligen Karte in Form eines Strings zurück.

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Der Wert der Karte
        """
        if self.value == 0:
            return "10"
        if self.value == 1:
            return "Ass"
        if self.value == 10:
            return "Bube"
        if self.value == 11:
            return "Dame"
        if self.value == 12:
            return "König"
        if self.value == 50:
            return "Joker"
        return str(self.value)


class Deck:
    def __init__(self,
                 empty: bool = False,
                 shuffled: bool = False):
        """
        Ein Kartendeck.

        :param empty: Gibt an, ob das Kartendeck beim Erstellen leer bleiben soll.
        :param shuffled: Gibt an, ob das Kartendeck nach dem Erstellen gemischt werden soll.
        """
        self.cards: list[Karte, ...] = []

        # Füge alle Karten zu dem Deck hinzu
        if not empty:
            self.new_deck()
        # Mische das Deck
        if shuffled and not empty:
            self.shuffle()

    def __repr__(self) -> str:
        """
        Was bei ``str(Deck)`` bzw ``print(Deck)`` zurückgegeben wird, z.B.:

        >>> deck = Deck()
        >>> print(deck)
        'Deck(cards=[Karte(suit=0, value=0), ...])'

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Eine String-Repräsentation des Objekts
        """
        return f"{self.__class__.__name__}(cards={self.cards})"

    def new_deck(self, clear: bool = False):
        """
        Fügt Standard-Pokerkarten zum Deck hinzu (von 2 bis Ass)

        :param clear: Gibt an, ob das Deck zunächst geleert werden soll, bevor die neuen Karten hinzugefügt werden
        :return: Nichts
        """
        if clear:
            self.cards = []
        self.cards += [Karte(suit=suit, value=value) for suit in range(4) for value in range(13)]
        self.cards += [Karte(suit=None, value=50), Karte(suit=None, value=50)]

    def shuffle(self) -> None:
        """Mischt das Kartendeck."""
        shuffle(self.cards)

    def deal(self) -> Karte | None:
        """Entfernt die oberste Karte vom Stapel und returnt sie"""
        if self.cards:
            return self.cards.pop(0)
        return

    def add_card_at_top(self, karte: Karte):
        """Lege eine Karte oben auf das Deck"""
        self.cards.insert(0, karte)

    def add_card_at_bottom(self, karte: Karte):
        """Lege eine Karte unter das Deck"""
        self.cards.append(karte)


class Player:
    def __init__(self,
                 playerno: int,
                 name: str = "",
                 hand: list[Karte, ...] = None):
        """
        Ein Spieler.

        :param playerno: Die Nummer des Spielers
        :param name: Der Name des Spielers
        :param hand: Die Hand des Spielers
        """
        # Nummer (ID) des Spielers
        self.number = playerno
        # Name des Spielers
        if not name:
            name = f"Spieler {self.number}"
        self.name = name
        # Hand des Spielers
        if not hand:
            hand = []
        self.hand = hand

    def __repr__(self):
        return f'{self.__class__.__name__}(number={self.number}, name="{self.name}", hand={self.hand})'

    def take_card(self, karte: Karte):
        """Fügt eine Karte zur Hand des Spielers hinzu"""
        self.hand.append(karte)

    def play_card_at_index(self, index: int) -> Karte | None:
        """Entfernt die Karte aus der Hand des Spielers am gegebenen Index und returnt sie"""
        if 0 <= index <= len(self.hand) - 1:
            return self.hand.pop(index)
        return


class Game:
    def __init__(self,
                 players: int = 4,
                 anfangskarten: int = 4):
        """
        Initialisiere das Spiel Castor.

        :param players: Die Anzahl an Spielern
        :param anfangskarten: Die Anzahl an Karten, die jeder Spieler zu Beginn bekommt.
        """
        # Erstelle ein Kartendeck
        self.deck = Deck(empty=False, shuffled=True)
        # Erstelle einen Nachziehstapel
        self.stapel = Deck(empty=True)
        # Erstelle die Spieler
        self.spieler = [Player(playerno=i+1) for i in range(players)]
        # Beginne mit x Karten pro Spieler
        self.anfangskarten = anfangskarten

    def deal_cards_to_all(self):
        """Gibt jedem Spieler zu Beginn des Spiels seine Karten"""
        for s in self.spieler:
            for _ in range(self.anfangskarten):
                s.take_card(self.deck.deal())
