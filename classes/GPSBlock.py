# gps byte precision
#  4 bytes ~= 300m ~= dorp / wijk
#  5 bytes ~= 30m ~= gebouwen
#  6 bytes ~= 3m ~= auto, persoon, plek

# block optcodes
GPS_BLOCK_4 = 0x11
GPS_BLOCK_5 = 0x12
GPS_BLOCK_6 = 0x13
GPS_BLOCK_7 = 0x14


class GPSBlock():

  def __init__(self, value, bytes_precision = 6):
    
    self.bytes_precision = bytes_precision
    if bytes_precision < 4 or bytes_precision > 7:
        raise ValueError("Bytes precision must be between 4 and 7")

    self.max_val = 2 ** (bytes_precision * 4) - 1

    if isinstance(value, bytes):
      self.load_encoded_gps_coordinates(value)
    if isinstance(value, list):
      self.load_gps_coordinates(value[0], value[1])


  def encode(self):
    encoded = (self.lat_encoded << (self.bytes_precision * 4)) | self.lon_encoded
    
    if self.bytes_precision == 4:
      block_type = GPS_BLOCK_4
    if self.bytes_precision == 5:
      block_type = GPS_BLOCK_5
    if self.bytes_precision == 6:
      block_type = GPS_BLOCK_6
    if self.bytes_precision == 7:
      block_type = GPS_BLOCK_7
    
    return block_type.to_bytes(1) + encoded.to_bytes(self.bytes_precision)

  def decode(self):

    latitude = (self.lat_encoded / self.max_val) * 180 - 90
    longitude = (self.lon_encoded / self.max_val) * 360 - 180

    latitude = round(latitude, 6)
    longitude = round(longitude, 6)
    
    return str("('GPS') %s, %s" % (str(latitude), str(longitude)))


  def load_gps_coordinates(self, latitude, longitude):

    self.lat_encoded = int(((latitude + 90) / 180) * self.max_val)
    self.lon_encoded = int(((longitude + 180) / 360) * self.max_val)
    
  def load_encoded_gps_coordinates(self, encoded_bytes):

    encoded = int.from_bytes(encoded_bytes)

    self.lat_encoded = encoded >> (self.bytes_precision * 4)
    self.lon_encoded = encoded & self.max_val
