import time
from random import shuffle
from pprint import pprint
import sys
import telepot
from telepot.loop import MessageLoop
from tarotdeck import TarotDeck


class Sybil:
    def __init__(self):
        token = sys.argv[1]
        self.deck_type = 'jodocamoin'
        self.deck = TarotDeck(self.deck_type)
        shuffle(self.deck)
        self.composition = 'full_deck'
        self.bot = telepot.Bot(token)
        MessageLoop(self.bot, self.handle).run_as_thread()
        print('Listening ...')

    def majors(self, chat_id):
        self.bot.sendMessage(chat_id, 'Setting deck to Majors only')
        self.deck = TarotDeck(self.deck_type)[57:]
        shuffle(self.deck)
        self.composition = 'majors'

    def minors(self, chat_id):
        self.bot.sendMessage(chat_id, 'Setting deck to Minors only')
        self.deck = TarotDeck(self.deck_type)[:56]
        shuffle(self.deck)
        self.composition = 'minors'

    def full_deck(self, chat_id):
        self.bot.sendMessage(chat_id, 'Using full deck')
        self.deck = TarotDeck(self.deck_type)
        shuffle(self.deck)
        self.composition = 'full_deck'

    def set_deck(self, chat_id):
        if self.composition == 'majors:':
            self.majors(chat_id)
        elif self.composition == 'minors':
            self.minors(chat_id)
        else:
            self.full_deck(chat_id)
        shuffle(self.deck)

    def handle(self, message):
        content_type, chat_type, chat_id = telepot.glance(message)

        if content_type == 'text':
            
            pprint(message)
            
            message_text = message['text']
            message_lower = message_text.lower()
            command_tokens = message_lower.split()
            
            if command_tokens[0] in ('/majors', '/majors@sybilbot'): 
                self.composition = 'majors'
                self.set_deck(chat_id)
            
            elif command_tokens[0] in ('/minors', '/majors@sybilbot'):
                self.composition = 'minors'
                self.set_deck(chat_id)
            
            elif command_tokens[0] in ('/full' or '/full@sybilbot'):
                self.composition = 'full_deck'
                self.set_deck(chat_id)
            
            elif command_tokens[0] in ('/shuffle', '/shuffle@sybilbot'):
                self.set_deck(self.composition)
                self.bot.sendMessage(chat_id, 'Shuffling the deck...')
            
            elif command_tokens[0] in ('/settype', '/settype@sybilbot'):
                try:
                    if command_tokens[1] not in self.deck.deckRef.keys():
                        self.bot.sendMessage(chat_id, 'Invalid deck type')
                    else:
                        self.deck_type = command_tokens[1]
                        self.composition = 'full_deck'
                        self.set_deck(chat_id)
                except IndexError:
                    self.bot.sendMessage(chat_id, 'Invalid deck type')

            elif command_tokens[0] in ('/draw', '/draw@sybilbot'):
                if len(self.deck) > 0:
                    card = self.deck.pop()
                    if 'majors' not in card.image:
                        caption = card.rank + ' of ' + card.kind
                    else:
                        caption = card.rank + ': ' + card.kind
                    self.bot.sendPhoto(chat_id, open(card.image, 'rb'), caption=caption)
                else:
                    self.bot.sendMessage(chat_id, 'The deck is out of cards!')
            
            elif command_tokens[0] in ('/listtypes', '/listtypes@sybilbot'):
                decklist = ""
                for entry in self.deck.deckRef.keys():
                    decklist += "{}: {}\n".format(entry, self.deck.deckRef[entry][3])
                self.bot.sendMessage(chat_id, decklist)
            
            elif command_tokens[0] in ('/help', '/help@sybilbot'):
                self.bot.sendMessage(chat_id,
                                     "All commands are prefixed by a forward slash (/), with no spaces between the " +
                                     "slash and your command.  Currently I only deal from one deck.  Drawn cards " +
                                     "remain out of the deck until either someone issues a 'Majors', 'Minors', " +
                                     "'Full', 'Settype', or 'Shuffle' command.\n " +
                                     "These are the commands I currently understand:\n\n" +
                                     "Majors -- Set deck to deal only from the Major Arcana\n" +
                                     "Minors -- Set deck to deal only the pips\n" +
                                     "Full -- Set deck to deal both Majors and Minors\n" +
                                     "Listtypes -- List the types of decks available for use\n" +
                                     "Settype [type] -- Sets to one of the decks listed in Listtypes, eg: /settype" +
                                     "jodocamoin Note: This reshuffles the deck\n" +
                                     "Draw -- Draw a card\n" +
                                     "Help -- This text\n")

if __name__ == '__main__':
    # Keep the program running.
    telebot = Sybil()
    while 1:
        time.sleep(1)
