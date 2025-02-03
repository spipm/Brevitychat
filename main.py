from rich import print
from datetime import datetime

from classes.MessageEncoder import MessageEncoder
from classes.MessageDecoder import MessageDecoder
from classes import Languages

# create message from blocks
encoder = MessageEncoder(language = Languages.NL)

# encoder.add_legacytextblock('This is a test message!')
encoder.add_textblock('This is a test message!')
encoder.add_numberblock(1337)
encoder.add_endline()

encoder.add_dictblock('info',   'Wees op de hoogte van')
encoder.add_dictblock('marker', 'verzamelpunt')
encoder.add_gpsblock( 52.359121, 4.884078)
encoder.add_dictblock('req',    'Wat is je verwachte tijd van aankomst?')
encoder.add_endline()

encoder.add_dictblock('cmd',    'Geef mij meer informatie over')
encoder.add_linkblock('github.com')
encoder.add_endline()

encoder.add_dictblock('info',   'Verstuurd op')
encoder.add_dateblock(int(datetime.now().timestamp()))

encoded_message = encoder.generate_encoded_message()

# transmit
# ..
# receive

# decode
print("\n[%s]" % ('-' * len(encoded_message)))
print('\tIncoming message - (%s encoded bytes)\n' % len(encoded_message))

lines = MessageDecoder(encoded_message).decode()
for message_line in lines:
  print(message_line)

