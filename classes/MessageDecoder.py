from classes import dict_by_index
from classes import single_optcodes, dict_by_name
from classes.DictBlock import DictBlock
from classes.NumberBlock import NumberBlock, NUMBER_BLOCK
from classes.DateBlock import DateBlock, DATE_BLOCK
from classes.GPSBlock import GPSBlock, GPS_BLOCK_6
from .LegacyTextBlock import LegacyTextBlock, TEXT_BLOCK_LEGACY
from .TextBlock import TextBlock, TEXT_BLOCK
from classes.LinkBlock import LinkBlock, LINK_BLOCK

import zlib

from . import CompressionAlgo
from . import VERSION

from classes._helpers import decode_byte_to_fourbits



class MessageDecoder():
  
  def __init__(self, encoded_message):

    self.encoded_message = encoded_message

    self.version, self.language = decode_byte_to_fourbits(encoded_message[0])
    assert self.version == VERSION

    self.compression_method, self.reserved = decode_byte_to_fourbits(encoded_message[1])

    self.encoded_lines = encoded_message[2:]
    if self.compression_method == CompressionAlgo.GZIP:
      self.encoded_lines = zlib.decompress(self.encoded_lines)


  def decode(self):

    # decoding
    current_index = 0
    decoded_lines = []
    decoded_line = []

    encoded_lines = self.encoded_lines

    while current_index < len(encoded_lines):

      optcode = encoded_lines[current_index]

      # decode dictionary reference
      if optcode in dict_by_index:

        dict_choice = DictBlock(optcode, language = self.language)
        index_byte = encoded_lines[current_index+1]
        
        decoded = dict_choice.decode(index_byte)
        decoded_line.append(decoded)

        current_index += 2

      elif optcode == GPS_BLOCK_6:
        encoded_coordinates = encoded_lines[current_index+1:current_index+7]
        
        decoded = GPSBlock(encoded_coordinates).decode()
        decoded_line.append(decoded)
        
        current_index += 7

      elif optcode in single_optcodes:
        optcode_value = single_optcodes[optcode]
        
        decoded_line.append(optcode_value)

        # End of line
        if optcode == 0x00:
          decoded_lines.append(decoded_line)
          decoded_line = []
        
        current_index += 1

      elif optcode == DATE_BLOCK:
        encoded_timestamp = encoded_lines[current_index+1:current_index+5]
        
        decoded = DateBlock(encoded_timestamp).decode()
        decoded_line.append(decoded)

        current_index += 5

      # OPTODO: refactor following four blocks into one because the codeblocks are the same
      elif optcode == NUMBER_BLOCK:
        length = encoded_lines[current_index+1]
        
        encoded_number = encoded_lines[current_index+2:current_index+length+2]
        decoded = NumberBlock(encoded_number).decode()
        
        decoded_line.append(decoded)
        
        current_index += length+2


      elif optcode == TEXT_BLOCK_LEGACY:
        length = encoded_lines[current_index+1]

        encoded_text = encoded_lines[current_index+2:current_index+length+2]
        decoded = LegacyTextBlock(encoded_text).decode()

        decoded_line.append(decoded)
        
        current_index += length+2

      elif optcode == TEXT_BLOCK:
        length = encoded_lines[current_index+1]

        encoded_text = encoded_lines[current_index+2:current_index+length+2]
        decoded = TextBlock(encoded_text).decode()

        decoded_line.append(decoded)
        
        current_index += length+2

      elif optcode == LINK_BLOCK:
        length = encoded_lines[current_index+1]

        encoded_link = encoded_lines[current_index+2:current_index+length+2]
        decoded = LinkBlock(encoded_link).decode()

        decoded_line.append(decoded)
        
        current_index += length+2

      else:
        print("Error: unknown optcode: %s" % hex(optcode))
        current_index += 1

    if decoded_line not in decoded_lines:
      decoded_lines.append(decoded_line)

    lines = []
    for decoded_line in decoded_lines:
      lines.append( ' '.join(decoded_line).replace('EOL','') )

    return lines

