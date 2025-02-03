import unishox2


TEXT_BLOCK = 0x19

class TextBlock:

  def __init__(self, value):

    if isinstance(value, bytes):
      self.encoded = value
    if isinstance(value, str):
      self.plaintext = value
  
  def encode(self):
    encoded, original_length = unishox2.compress(self.plaintext)
    encoded_and_len = original_length.to_bytes(1) + encoded
    return TEXT_BLOCK.to_bytes(1) + len(encoded_and_len).to_bytes(1) + encoded_and_len

  def decode(self):
    original_length = self.encoded[0]
    encoded = self.encoded[1:]
    plaintext = unishox2.decompress(encoded, original_length)
    return plaintext


