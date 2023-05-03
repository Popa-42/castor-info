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
        state = {"suit": self.suit, "value": self.value}
        return f"{state}"

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
                 number: int,
                 name: str = "",
                 hand: list[Card, ...] = None):
        """
        Ein Spieler.

        :param number: Die Nummer des Spielers
        :param name: Der Name des Spielers
        :param hand: Die Hand des Spielers
        """
        # Nummer (ID) des Spielers
        self.number = number
        # Name des Spielers
        if not name:
            name = f"Spieler {self.number}"
        self.name = name
        # Hand des Spielers
        if not hand:
            hand = []
        self.hand = hand

    def __repr__(self):
        state = {"number": self.number, "name": self.name, "hand": self.hand}
        return f"{state}"

    def take_card(self, karte: Card):
        """Fügt eine Karte zur Hand des Spielers hinzu"""
        self.hand.append(karte)

    def play_card_at_index(self, index: int) -> Card | None:
        """Entfernt die Karte aus der Hand des Spielers am gegebenen Index und returnt sie"""
        if 0 <= index <= len(self.hand) - 1:
            return self.hand.pop(index)
        return


class Game:
    def __init__(self,
                 players: int = 4,
                 anfangskarten: int = 4,
                 erster_spieler: int = 0):
        """
        Initialisiert das Spiel Castor:

        - Erstellt (standardmäßig vier) :class:`Player`
        - Erstellt ein volles :class:`Deck` Karten (der Nachziehstapel)
        - Erstellt ein leeres Deck Karten (der Ablagestapel)
        - Teilt jedem der Spieler (standardmäßig vier) Karten aus

        :param players: Die Anzahl an Spielern
        :param anfangskarten: Die Anzahl an Karten, die jeder Spieler zu Beginn bekommt.
        :param erster_spieler: Der Index desjenigen Spielers, der beginnt
        """
        # Erstelle einen Nachziehstapel (Oberste Karte: Index 0)
        self.deck: list[Card, ...] = [Card(suit=s, value=v) for s in range(4) for v in range(13)]
        self.deck += [Card(None, 50), Card(None, 50)]
        shuffle(self.deck)
        # Erstelle einen Ablagestapel
        self.ablage: list[Card, ...] = []
        # Erstelle die Player
        self.players = [Player(number=i + 1) for i in range(players)]
        # Der erste Spieler
        self.current_player = erster_spieler
        # Beginne mit x Karten pro Spieler
        self.anfangskarten = anfangskarten
        # Ob das Spiel gewonnen wurde
        self.game_won = False

    def __repr__(self) -> str:
        state = {
            "deck": self.deck,
            "ablage": self.ablage,
            "players": self.players,
            "anfangskarten": self.anfangskarten,
            "current_player": self.current_player,
            "game_won": self.game_won,
        }
        return f"{state}"

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
        return self.players[self.current_player]

    def export_current_state(self) -> bytes:
        state = self.__repr__()
        return state.encode()

    def import_state(self, save: bytes):
        # Convert imported bytes to dict
        game: dict = eval(save.decode())
        # Import Players from dict
        players = game["players"]
        self.players = [Player(
            number=p["number"],
            hand=[Card(suit=c["suit"], value=c["value"]) for c in p["hand"]],
            name=p["name"]
        ) for p in players]
        # Import deck from dict
        deck = game["deck"]
        if deck:
            self.deck = [Card(suit=c["suit"], value=c["value"]) for c in deck]
        else:
            self.deck = []
        # Import Ablage from dict
        ablage = game["ablage"]
        if ablage:
            self.ablage = [Card(suit=c["suit"], value=c["value"]) for c in ablage]
        else:
            self.ablage = []
        self.anfangskarten = game["anfangskarten"]
        self.current_player = game["current_player"]
        # Import whether the game was won
        self.game_won = game["game_won"]
