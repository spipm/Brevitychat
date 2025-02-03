from os import path

from . import dict_by_index
from . import dict_by_name
from . import Languages


language_map = {
  Languages.NL : 'nl',
  Languages.EN : 'en'
}

# Block in the format [1byte OPTCODE][1byte DICT INDEX]
class DictBlock():

  def __init__(self, reference, language = Languages.NL):

    self.language   = language
    
    self.dict_index = 0x00
    self.dictname   = ''
    self.dictlines  = []

    # Load the dict in mem
    if isinstance(reference, str):
      self.dictname  = reference
      self.load_from_dictname()

    if isinstance(reference, int):
      self.dict_index = reference
      self.load_from_optcode()


  def return_dictionary_in_mem(self):

    filepath = path.join(
                  'dictionaries',
                  language_map[self.language],
                  self.filename
                )

    with open(filepath, 'r') as fin:
      self.dictlines = fin.read().split('\n')


  # dict in format 'SOS': [0x21, '_dict_sos'],
  def load_from_dictname(self):

    entry           = dict_by_name[self.dictname]
    self.dict_index = entry[0]
    self.filename   = entry[1]
    self.return_dictionary_in_mem()

  def load_from_optcode(self):

    entry         = dict_by_index[self.dict_index]
    self.dictname = entry[0]
    self.filename = entry[1]
    self.return_dictionary_in_mem()


  def encode(self, value): 
    value_index = self.dictlines.index(value)
    return self.dict_index.to_bytes(1) + value_index.to_bytes(1)

  def decode(self, value_index):
    return "('%s') %s" % (self.dictname.upper(), self.dictlines[value_index])

