# Das Backend für Castor
# → Das grundlegende Kartenspiel

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
        if self.suit is None:
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
    def __init__(self, empty: bool = False):
        """
        Ein Kartendeck.

        :param empty: Gibt an, ob das Kartendeck beim Erstellen leer bleiben soll.
        """
        self.cards: list[Karte, ...] = []

        # Füge alle Karten zu dem Deck hinzu
        if not empty:
            self.new_deck()

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
