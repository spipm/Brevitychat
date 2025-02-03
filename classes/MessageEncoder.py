import zlib
import enum

from . import CompressionAlgo
from . import Languages
from . import VERSION
from . import EOL

from .NumberBlock import NumberBlock, NUMBER_BLOCK
from .DateBlock import DateBlock, DATE_BLOCK
from .LegacyTextBlock import LegacyTextBlock, TEXT_BLOCK_LEGACY
from .TextBlock import TextBlock, TEXT_BLOCK
from .LinkBlock import LinkBlock, LINK_BLOCK
from .GPSBlock import GPSBlock, GPS_BLOCK_6
from .DictBlock import DictBlock

from ._helpers import encode_fourbits_to_byte


class MessageEncoder():

  def __init__(self, language = Languages.NL):
    self.blocks = []
    self.language = language
    self.compression_method = CompressionAlgo.NONE


  # this byte consists of the version and the language for the dictionaries
  def wrap_versionbyte(self, plainbytes):

    version_byte = encode_fourbits_to_byte(VERSION, self.language).to_bytes(1)
    
    return version_byte + plainbytes

  # this byte consists of the compression and a non-defined value
  def wrap_compressionbyte(self, plainbytes):
    reserved = 0
    compression_byte = encode_fourbits_to_byte(self.compression_method, reserved).to_bytes(1)
    
    return compression_byte + plainbytes

  def generate_encoded_message(self):

    encoded_lines = b''.join([x for x in self.blocks])

    line_compressed = zlib.compress(encoded_lines)

    if len(encoded_lines) > len(line_compressed):
      encoded_lines = line_compressed
      self.compression_method = CompressionAlgo.GZIP

    return self.wrap_versionbyte(
              self.wrap_compressionbyte(
                encoded_lines
              )
            )

  def add_dictblock(self, dictname, entry_value):
    block = DictBlock(
              dictname,
              language = self.language
              ).encode(entry_value)
    self.blocks.append(block)

  def add_textblock(self, text):
    block = TextBlock(text).encode()
    self.blocks.append(block)

  def add_legacytextblock(self, text):
    block = LegacyTextBlock(text).encode()
    self.blocks.append(block)

  def add_gpsblock(self, latitude, longtitude):
    block = GPSBlock([latitude, longtitude]).encode()
    self.blocks.append(block)

  def add_dateblock(self, timestamp):
    block = DateBlock(timestamp).encode()
    self.blocks.append(block)

  def add_numberblock(self, number):
    block = NumberBlock(number).encode()
    self.blocks.append(block)

  def add_linkblock(self, link):
    block = LinkBlock(link).encode()
    self.blocks.append(block)

  def add_endline(self):
    self.blocks.append(EOL)

