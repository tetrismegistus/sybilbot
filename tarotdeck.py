import collections

Card = collections.namedtuple('card', ['rank', 'kind', 'image'])


class TarotDeck:
    def __init__(self, deck):
        self.set_cards(deck)
        self._cards = [Card(rank, suit, self.minor_image.format(suit, rank)) for suit in self.suits
                       for rank in self.ranks]
        self._cards += [Card(c[0], c[1], self.major_image.format(c[0])) for c in zip(self.numerals, self.titles)]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, key, value):
        self._cards[key] = value

    def pop(self, key=-1):
        card = self._cards.pop(key)
        return card

    def set_cards(self, deck):
        path = 'images/{}/'.format(deck)
        self.minor_image = path + '{}/{}.jpg'
        self.major_image = path + 'majors/{}.jpg'

        suitDict = {'traditional': 'swords staves coins cups'.split(),
                    'riderwaite': 'swords wands pentacles cups'.split(),
                    'crowleythoth': 'swords wands disks cups'.split()}

        courtDict = {'traditional': 'Page Queen King Knight'.split(),
                     'crowleythoth': 'Princess Prince Queen Knight'.split()}

        trumpDict = {'marseille': ['The Fool', 'The Magician', 'The Popess', 'The Empress', 'The Emperor',
                                   'The Pope', 'The Lover', 'The Chariot', 'Justice', 'The Hermit',
                                   'The Wheel of Fortune', 'Strength', 'The Hanged Man', 'Death',
                                   'Temperance', 'The Devil', 'The House of God', 'The Star', 'The Moon',
                                   'The Sun', 'Judgement', 'The World'],
                     'riderwaite': ['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor',
                                    'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit',
                                    'The Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death',
                                    'Temperance', 'The Devil', 'The Tower', 'The Star', 'The Moon',
                                    'The Sun', 'Judgement', 'The World'],
                     'crowleythoth': ['The Fool', 'The Magus', 'The Priestess', 'The Empress', 'The Emperor',
                                      'The Hierophant', 'The Lovers', 'The Chariot', 'Adjustment', 'The Hermit',
                                      'Fortune', 'Lust', 'The Hanged Man', 'Death', 'Art', 'The Devil',
                                      'The Tower', 'The Star', 'The Moon', 'The Sun', 'The Aeon', 'The Universe']}

        # 0 = suits, 1 = courts, 2 = trumps, 3 = description
        self.deckRef = {'jodocamoin': [suitDict['traditional'], 
                                       courtDict['traditional'], 
                                       trumpDict['marseille'],
                                       "A Marseille deck by Jodorowsky & Camoin"],
                        'riderwaitesmith': [suitDict['riderwaite'], 
                                            courtDict['traditional'], 
                                            trumpDict['riderwaite'],
                                            "The Rider-Waite-Smith deck"],
                        'crowleythoth': [suitDict['crowleythoth'],
                                         courtDict['crowleythoth'],
                                         trumpDict['crowleythoth'],
                                         "The Crowley Thoth deck"]}

        self.numerals = [str(n) for n in range(0, 22)]
        self.ranks = ['Ace'] + [str(n) for n in range(2, 11)] + self.deckRef[deck][1]
        self.titles = self.deckRef[deck][2]
        self.suits = self.deckRef[deck][0]



