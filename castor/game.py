# Das Backend für Castor
# → Das grundlegende Kartenspiel

from random import shuffle


class Card:
    def __init__(self,
                 farbe: int | None,
                 wert: int):
        """
        Eine Spielkarte mit Farbe und Wert.

        :param farbe: Die Farbe der Karte
        :param wert: Der Wert der Karte
        """
        self.farbe = farbe
        self.wert = wert

    def __repr__(self) -> str:
        """
        Was bei ``str(Karte)`` bzw ``print(Karte)`` zurückgegeben wird.
        Nützlich für den Export des aktuellen Spielstands für die
        Kommunikation zwischen Client und Server.

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Eine String-Repräsentation des Objekts
        """
        karte = {"farbe": self.farbe, "wert": self.wert}
        return f"{karte}"

    def suit_str(self) -> str:
        """
        Gibt die Farbe der jeweiligen Karte in Form eines Strings zurück.

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Die Farbe der Karte
        """
        if self.farbe == 0:
            return "Kreuz"
        if self.farbe == 1:
            return "Pik"
        if self.farbe == 2:
            return "Herz"
        if self.farbe == 3:
            return "Karo"
        if not self.farbe:
            return ""
        raise IndexError("Diese Farbe existiert nicht.")

    def value_str(self) -> str:
        """
        Gibt den Wert der jeweiligen Karte in Form eines Strings zurück.

        :param self: Bezieht sich auf die Instanz der Klasse
        :return: Der Wert der Karte
        """
        if self.wert == 0:
            return "10"
        if self.wert == 1:
            return "Ass"
        if self.wert == 10:
            return "Bube"
        if self.wert == 11:
            return "Dame"
        if self.wert == 12:
            return "König"
        if self.wert == 50:
            return "Joker"
        return str(self.wert)


class Player:
    def __init__(self,
                 nummer: int,
                 name: str = "",
                 hand: list[Card, ...] = None):
        """
        Ein Spieler.

        :param nummer: Die Nummer des Spielers
        :param name: Der Name des Spielers
        :param hand: Die Hand des Spielers
        """
        # Nummer (ID) des Spielers
        self.nummer = nummer
        # Name des Spielers
        if not name:
            name = f"Spieler {self.nummer}"
        self.name = name
        # Hand des Spielers
        if not hand:
            hand = []
        self.hand = hand

    def __repr__(self):
        state = {"nummer": self.nummer, "name": self.name, "hand": self.hand}
        return f"{state}"

    def take_card(self, karte: Card):
        """Fügt eine Karte zur Hand des Spielers hinzu"""
        self.hand.append(karte)

    def swap_card_with_index(self, card: Card, index: int) -> bool:
        """Versucht, eine Karte der Hand des Spielers hinzuzufügen. Returns bool für Erfolg"""
        try:
            self.hand[index] = card
            return True
        except IndexError:
            return False

    def play_card_at_index(self, index: int) -> Card | None:
        """Entfernt die Karte aus der Hand des Spielers am gegebenen Index und returnt sie"""
        if 0 <= index <= len(self.hand) - 1:
            return self.hand.pop(index)
        return

    def get_hand(self) -> list[list[str]]:
        liste = []
        for c in self.hand:
            liste.append([c.suit_str(), c.value_str()])
        return liste


class Game:
    def __init__(self,
                 spielerzahl: int = 4,
                 anfangskarten: int = 4,
                 erster_spieler: int = 0):
        """
        Initialisiert das Spiel Castor:

        - Erstellt (standardmäßig vier) :class:`Player`
        - Erstellt ein volles :class:`Deck` Karten (der Nachziehstapel)
        - Erstellt ein leeres Deck Karten (der Ablagestapel)
        - Teilt jedem der Spieler (standardmäßig vier) Karten aus

        :param spielerzahl: Die Anzahl an Spielern
        :param anfangskarten: Die Anzahl an Karten, die jeder Spieler zu Beginn bekommt.
        :param erster_spieler: Der Index desjenigen Spielers, der beginnt
        """
        # Erstelle einen Nachziehstapel (Oberste Karte: Index 0)
        self.deck: list[Card, ...] = [Card(farbe=s, wert=v) for s in range(4) for v in range(13)]
        self.deck += [Card(None, 50), Card(None, 50)]
        shuffle(self.deck)
        # Erstelle einen Ablagestapel
        self.ablage: list[Card, ...] = []
        # Erstelle die Player
        self.players = [Player(nummer=i + 1) for i in range(spielerzahl)]
        # Der erste Spieler
        self.current_player = erster_spieler
        # Beginne mit x Karten pro Spieler
        self.anfangskarten = anfangskarten
        # Ob das Spiel gewonnen wurde
        self.game_over = False
        # Wer den Joker gelegt hat
        self.first_joker_by: int = ...

    def __repr__(self) -> str:
        aktueller_stand = {
            "deck": self.deck,
            "ablage": self.ablage,
            "players": self.players,
            "anfangskarten": self.anfangskarten,
            "current_player": self.current_player,
            "game_over": self.game_over,
        }
        return f"{aktueller_stand}"

    def deal_cards_to_all(self):
        """Gibt jedem Spieler zu Beginn des Spiels seine Karten"""
        for s in self.players:
            for _ in range(self.anfangskarten):
                s.take_card(self.deck.pop(0))

    def draw_card(self) -> Card:
        """Zieht die oberste Karte des Decks. Wenn der Nachziehstapel leer ist, Ablagestapel mischen und neu benutzen"""
        if not self.deck and self.ablage:
            shuffle(self.ablage)
            self.deck = self.ablage
            self.ablage = []
        elif not self.deck and not self.ablage:
            raise Exception("Sowohl das Deck als auch der Ablagestapel sind leer.")
        return self.deck.pop(0)

    def draw_ablage(self) -> Card:
        """Zieht die oberste Karte vom Ablagestapel."""
        if self.ablage:
            return self.ablage.pop(0)

    def get_current_player(self) -> Player:
        """Gibt den aktuellen Spieler zurück"""
        return self.players[self.current_player]

    def next_player(self):
        """Der nächste Spieler"""
        self.current_player += 1
        self.current_player %= len(self.players)

    def export_current_state(self) -> bytes:
        state = self.__repr__()
        return state.encode()

    def import_state(self, save: bytes):
        # Convert imported bytes to dict
        game: dict = eval(save.decode())
        # Import Players from dict
        spielerliste = game["players"]
        self.players = [Player(
            nummer=p["nummer"],
            hand=[Card(farbe=c["farbe"], wert=c["wert"]) for c in p["hand"]],
            name=p["name"]
        ) for p in spielerliste]
        # Import deck from dict
        deck = game["deck"]
        if deck:
            self.deck = [Card(farbe=c["farbe"], wert=c["wert"]) for c in deck]
        else:
            self.deck = []
        # Import Ablage from dict
        ablage = game["ablage"]
        if ablage:
            self.ablage = [Card(farbe=c["farbe"], wert=c["wert"]) for c in ablage]
        else:
            self.ablage = []
        self.anfangskarten = game["anfangskarten"]
        self.current_player = game["current_player"]
        # Import whether the game was won
        self.game_over = game["game_over"]

    def end_game(self):
        self.game_over = True

    def first_joker_laid_by(self, player_index: int):
        self.first_joker_by = player_index

    def throw_card_to_ablage(self, card: Card):
        self.ablage.insert(0, card)

    def player_throws_card_at(self, player_index: int, index: int):
        card = self.players[player_index].play_card_at_index(index)
        self.throw_card_to_ablage(card)
