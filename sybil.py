import time
from random import shuffle
from pprint import pprint
import sys

import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_from_id, create_open, per_chat_id
from tarotdeck import TarotDeck


class Sybil(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decks = {}
        self.deck = {}
        self.from_id = 0

    def majors(self):
        self.sender.sendMessage('Setting your deck to Majors only')
        self.deck['deck_object'] = TarotDeck(self.deck['type'])[57:]

    def minors(self):
        self.sender.sendMessage('Setting your deck to Minors only')
        self.deck['deck_object'] = TarotDeck(self.deck['type'])[:56]

    def full_deck(self):
        self.sender.sendMessage('Setting your deck to both Majors and Minors')
        self.deck['deck_object'] = TarotDeck(self.deck['type'])

    def set_deck(self):
        if self.deck['composition'] == 'majors:':
            self.majors()
        elif self.deck['composition'] == 'minors':
            self.minors()
        else:
            self.full_deck()
        shuffle(self.deck['deck_object'])

    def on_chat_message(self, message):
        content_type, chat_type, chat_id = telepot.glance(message)
        from_id = message['from']['id']

        if from_id not in self.decks.keys():
            self.deck = {'type': 'jodocamoin', 'composition': 'full_deck', 'deck_object': TarotDeck('jodocamoin')}
            self.decks[from_id] = self.deck
            self.set_deck()
        else:
            self.deck = self.decks[from_id]

        if content_type == 'text':
            pprint(message)
            
            message_text = message['text']
            message_lower = message_text.lower()
            command_tokens = message_lower.split()
            
            if command_tokens[0] in ('/majors', '/majors@sybilbot'): 
                self.deck['composition'] = 'majors'
                self.set_deck()

            elif command_tokens[0] in ('/minors', '/majors@sybilbot'):
                self.deck['composition'] = 'minors'
                self.set_deck()
            
            elif command_tokens[0] in ('/full' or '/full@sybilbot'):
                self.deck['composition'] = 'full_deck'
                self.set_deck()
            
            elif command_tokens[0] in ('/shuffle', '/shuffle@sybilbot'):
                self.set_deck()
                self.sender.sendMessage('Shuffling the deck...')
            
            elif command_tokens[0] in ('/settype', '/settype@sybilbot'):
                try:
                    if command_tokens[1] not in self.deck['deck_object'].deckRef.keys():
                        self.sender.sendMessage('Invalid deck type')
                    else:
                        self.deck['type'] = command_tokens[1]
                        self.deck['composition'] = 'full_deck'
                        self.set_deck()
                except IndexError:
                    self.sender.sendMessage('Invalid deck type')

            elif command_tokens[0] in ('/draw', '/draw@sybilbot'):
                if len(self.deck['deck_object']) > 0:
                    card = self.deck['deck_object'].pop()
                    if 'majors' not in card.image:
                        caption = card.rank + ' of ' + card.kind
                    else:
                        caption = card.rank + ': ' + card.kind
                    self.sender.sendPhoto(open(card.image, 'rb'), caption=caption)
                else:
                    self.sender.sendMessage('The deck is out of cards!')
                self.sender.sendMessage('Your deck has {} cards left'.format(len(self.deck['deck_object'])))
            
            elif command_tokens[0] in ('/listtypes', '/listtypes@sybilbot'):
                decklist = ""
                for entry in self.deck['deck_object'].deckRef.keys():
                    decklist += "{}: {}\n".format(entry, self.deck['deck_object'].deckRef[entry][3])
                self.sender.sendMessage(decklist)
            
            elif command_tokens[0] in ('/help', '/help@sybilbot'):
                self.sender.sendMessage("All commands are prefixed by a forward slash (/), with no spaces between the" +
                                        " slash and your command.  Currently I only deal from one deck.  Drawn cards " +
                                        "remain out of the deck until either someone issues a 'Majors', 'Minors', " +
                                        "'Full', 'Settype', or 'Shuffle' command.\n " +
                                        "These are the commands I currently understand:\n\n" +
                                        "Majors -- Set deck to deal only from the Major Arcana\n" +
                                        "Minors -- Set deck to deal only the pips\n" +
                                        "Full -- Set deck to deal both Majors and Minors\n" +
                                        "Listtypes -- List the types of decks available for use\n" +
                                        "Settype [type] -- Sets to one of the decks listed in Listtypes, eg: /settype " +
                                        "jodocamoin Note: This reshuffles the deck\n" +
                                        "Draw -- Draw a card\n" +
                                        "Help -- This text\n")

            self.decks[from_id] = self.deck

if __name__ == '__main__':
    # token = sys.argv[1]
    token = '358115353:AAHsd-W_3jiYUXg_sABz5JIwkiR5yHAnm-A'
    sybil = telepot.DelegatorBot(token, [pave_event_space()(per_chat_id(), create_open, Sybil, timeout=600)])
    MessageLoop(sybil).run_as_thread()
    while 1:
        time.sleep(1)
