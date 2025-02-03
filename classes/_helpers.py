
def encode_fourbits_to_byte(a, b):
  return ((a << 4) & 0xff) | b

def decode_byte_to_fourbits(x):
  a = (x & 240) >> 4
  b = x & 15
  return a, b

