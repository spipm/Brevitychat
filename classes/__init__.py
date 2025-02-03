import enum


VERSION = 1

# 4-bit compression option
class CompressionAlgo(enum.IntEnum):
  NONE = 0x0
  GZIP = 0x1

# 4-bit language option
class Languages(enum.IntEnum):
  NL = 0x0
  EN = 0x1

# special single byte optcodes
single_optcodes = {
  0x00 : 'EOL'
}
encode_single_optcodes = {v: k for k, v in single_optcodes.items()}

EOL = encode_single_optcodes['EOL'].to_bytes(1)

# name, optcode and filename for dictionary blocks
dict_by_name = {
  'sos':      [0x31, '_dict_sos'],
  'req':      [0x32, '_dict_req'],
  'ack':      [0x33, '_dict_ack'],
  'warn':     [0x34, '_dict_warn'],
  'info':     [0x35, '_dict_info'],
  'cmd':      [0x36, '_dict_cmd'],
  
  'marker':   [0x41, '_dict_marker'],
  'meme':     [0x42, '_dict_meme']
}
dict_by_index = {v[0]: [k, v[1]] for k, v in dict_by_name.items()}

