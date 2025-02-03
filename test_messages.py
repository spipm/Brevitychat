# Test generating messages for different circumstances

from rich import print
from datetime import datetime, timedelta

from classes.MessageEncoder import MessageEncoder
from classes.MessageDecoder import MessageDecoder
from classes import Languages


messages = []


# Emergency message EN
one_week_from_now = datetime.now() + timedelta(weeks=1)
one_week_from_now = int(one_week_from_now.timestamp())

encoder = MessageEncoder(language = Languages.EN)

encoder.add_dictblock('sos', 'Medical - Severe injuries')
encoder.add_dictblock('sos', 'Medical - Multiple wounded')
encoder.add_numberblock(6)
encoder.add_gpsblock(52.0907, 5.1214)
encoder.add_textblock('Building number is')
encoder.add_numberblock(12341337)
encoder.add_endline()

encoder.add_dictblock('cmd', 'Move to the location')
encoder.add_dictblock('req', 'What is your estimated time of arrival?')
encoder.add_endline()

encoder.add_dictblock('marker', 'assembly point')
encoder.add_gpsblock(51.0907, 4.1214)
encoder.add_endline()

encoder.add_dictblock('info', 'Sent on')
encoder.add_dateblock(int(datetime.now().timestamp()))

messages.append(encoder.generate_encoded_message())

# Emergency message NL
one_week_from_now = datetime.now() + timedelta(weeks=1)
one_week_from_now = int(one_week_from_now.timestamp())

encoder = MessageEncoder(language = Languages.NL)

encoder.add_dictblock('sos', 'Medisch - Zwaargewond')
encoder.add_dictblock('sos', 'Medisch - Meerdere gewonden:')
encoder.add_numberblock(6)
encoder.add_gpsblock(52.0907, 5.1214)
encoder.add_endline()

encoder.add_dictblock('cmd', 'Beweeg naar locatie')
encoder.add_dictblock('req', 'Heb je water voor ons?')
encoder.add_dictblock('req', 'Wat is je verwachte tijd van aankomst?')
encoder.add_endline()

encoder.add_dictblock('info', 'Weg afgesloten')
encoder.add_dictblock('info', 'Veilige route via')
encoder.add_textblock('A22')
encoder.add_gpsblock(51.0907, 6.1214)
encoder.add_textblock(', 06 voor updates is')
encoder.add_numberblock(612323345)
encoder.add_endline()

encoder.add_dictblock('warn', 'Vijanden gespot')
encoder.add_gpsblock(52.3907, 5.4214)
encoder.add_dictblock('warn', 'Een grote vijandelijke macht van onbekende grootte en formatie')
encoder.add_endline()

encoder.add_dictblock('marker', 'verzamelpunt')
encoder.add_dictblock('marker', 'neutraal')
encoder.add_gpsblock(51.0907, 4.1214)
encoder.add_endline()

encoder.add_dictblock('info', 'Verstuurd op')
encoder.add_dateblock(int(datetime.now().timestamp()))

messages.append(encoder.generate_encoded_message())

# Party message
encoder = MessageEncoder(language = Languages.NL)

encoder.add_dictblock('info',   'Wees op de hoogte van')
encoder.add_dictblock('marker', 'feest')
encoder.add_gpsblock( 52.0907, 5.1214)
encoder.add_dateblock(one_week_from_now)
encoder.add_endline()
encoder.add_dictblock('info', 'Voor meer informatie zie')
encoder.add_linkblock('test.com/?rdr=deadbeef')
encoder.add_endline()
encoder.add_textblock('😎 wij zijn met')
encoder.add_numberblock(100)
encoder.add_dictblock('req', 'Kom jij ook?')
encoder.add_dictblock('req', 'Wat is je verwachte tijd van aankomst?')
encoder.add_endline()
encoder.add_dictblock('cmd','Geef mij meer informatie over')
encoder.add_dictblock('marker', 'verblijf')
encoder.add_endline()

messages.append(encoder.generate_encoded_message())

import binascii

for encoded_message in messages:

  print("\n[%s]" % ('-' * len(encoded_message)))
  print('\tIncoming message - (%s encoded bytes)\n' % len(encoded_message))

  print(binascii.hexlify(encoded_message))

  lines = MessageDecoder(encoded_message).decode()
  for message_line in lines:
    print(message_line)


