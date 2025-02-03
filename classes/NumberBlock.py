NUMBER_BLOCK = 0x16

class NumberBlock():

  def __init__(self, value):

    if isinstance(value, bytes):
      self.number_bytes = value
    if isinstance(value, int):
      self.number = value


  def encode(self) -> bytes:

    bytes_amount    = (self.number.bit_length() + 7) // 8
    number_as_bytes =  self.number.to_bytes(bytes_amount)
    
    return NUMBER_BLOCK.to_bytes(1) + bytes_amount.to_bytes(1) + number_as_bytes

  def decode(self) -> int:
    return str(int.from_bytes(self.number_bytes))

