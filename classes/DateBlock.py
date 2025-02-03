import time
import struct
from datetime import datetime

# optcode
DATE_BLOCK = 0x15


# timestamp to and from 4-byte integer (seconds since epoch)
class DateBlock():

  def __init__(self, value):
    
    if isinstance(value, bytes):
      self.encoded_timestamp = value

    if isinstance(value, int):
      self.timestamp = value


  def encode(self) -> bytes:
    
    if self.timestamp == 0:
      self.timestamp = time.time()
    
    return DATE_BLOCK.to_bytes(1) + struct.pack('>I', int(self.timestamp))


  def decode(self, to_date = True) -> float:
    
    timestamp = float(struct.unpack('>I', self.encoded_timestamp)[0])
    
    if to_date:
      return str(datetime.fromtimestamp(timestamp))
    
    else:
      return str(timestamp)