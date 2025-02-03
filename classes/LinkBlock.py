import zlib


LINK_BLOCK = 0x17

class LinkBlock():

  def __init__(self, value):
    
    self.value = value

  def encode(self):
      encoded = zlib.compress(self.value.encode('utf-8'))
      return LINK_BLOCK.to_bytes(1) + len(encoded).to_bytes(1) + encoded

  def decode(self):
      decoded = zlib.decompress(self.value).decode('utf-8')
      return decoded

