# Das Backend für Castor
# → Das grundlegende Kartenspiel

from random import shuffle


class Card:
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

        >>> karte = Card(suit=1, value=1)
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


class Player:
    def __init__(self,
                 playerno: int,
                 name: str = "",
                 hand: list[Card, ...] = None,
                 turn: bool = False):
        """
        Ein Spieler.

        :param playerno: Die Nummer des Spielers
        :param name: Der Name des Spielers
        :param hand: Die Hand des Spielers
        :param turn: Gibt an, ob der Spieler an der Reihe ist
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
        self.turn = turn

    def __repr__(self):
        return f'{self.__class__.__name__}(number={self.number}, name="{self.name}", hand={self.hand})'

    def take_card(self, karte: Card):
        """Fügt eine Karte zur Hand des Spielers hinzu"""
        self.hand.append(karte)

    def play_card_at_index(self, index: int) -> Card | None:
        """Entfernt die Karte aus der Hand des Spielers am gegebenen Index und returnt sie"""
        if 0 <= index <= len(self.hand) - 1:
            return self.hand.pop(index)
        return

    def set_turn(self, turn: bool):
        """Setzt den Spieler auf aktiv ("an der Reihe")"""
        self.turn = turn

    def get_turn(self) -> bool:
        return self.turn


class Game:
    def __init__(self,
                 players: int = 4,
                 anfangskarten: int = 4,
                 first_player: int = 0):
        """
        Initialisiert das Spiel Castor:

        - Erstellt (standardmäßig vier) :class:`Player`
        - Erstellt ein volles :class:`Deck` Karten (der Nachziehstapel)
        - Erstellt ein leeres Deck Karten (der Ablagestapel)
        - Teilt jedem der Spieler (standardmäßig vier) Karten aus

        :param players: Die Anzahl an Spielern
        :param anfangskarten: Die Anzahl an Karten, die jeder Spieler zu Beginn bekommt.
        :param first_player: Der Index desjenigen Spielers, der beginnt
        """
        # Erstelle einen Nachziehstapel (Oberste Karte: Index 0)
        self.deck: list[Card, ...] = [Card(suit=s, value=v) for s in range(4) for v in range(13)]
        self.deck += [Card(None, 50), Card(None, 50)]
        shuffle(self.deck)
        # Erstelle einen Ablagestapel
        self.ablage: list[Card, ...] = []
        # Erstelle die Player
        self.players = [Player(playerno=i + 1) for i in range(players)]
        self.players[first_player].set_turn(True)
        # Beginne mit x Karten pro Spieler
        self.anfangskarten = anfangskarten

    def deal_cards_to_all(self):
        """Gibt jedem Spieler zu Beginn des Spiels seine Karten"""
        for s in self.players:
            for _ in range(self.anfangskarten):
                s.take_card(self.deck.pop(0))

    def draw_card(self) -> Card:
        """Zieht die oberste Karte des Decks. Wenn der Nachziehstapel leer ist, Ablagestapel mischen und neu benutzen"""
        if not self.deck:
            shuffle(self.ablage)
            self.deck = self.ablage
            self.ablage = []
        return self.deck.pop(0)

    def get_current_player(self) -> Player:
        """Gibt den aktuellen Spieler zurück"""
        for player in self.players:
            if player.get_turn():
                return player
        raise Exception("Etwas ist schiefgelaufen: Kein Spieler ist aktuell an der Reihe.")
