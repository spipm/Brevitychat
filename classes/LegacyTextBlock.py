import re
from os import path

# Custom text compressor, replaced by Unishox2 (also used by meshtastic)

# optcode
TEXT_BLOCK_LEGACY = 0x18

# twee byte dict is doorgaans efficienter dan switchen tussen dicts
# ds a a b b c c 0 0 dd d 0 ds e e f f ..
# ds a a b b c c d d e  e f f ..


# Original by me, optimized by Claud

import re

normalizations_text_patterns = [
    # nl
    (re.compile(r'[\u201C\u201D]'), '"'),
    (re.compile(r'[\u2014\+]'), '-'),
    (re.compile(r'[\u2018\u2019]'), "'"),
    (re.compile(r'\'t'), 'het'),
    (re.compile(r'\'n'), 'een'),
    (re.compile(r'z\'n'), 'zijn'),
    (re.compile(r'd\'r'), 'haar'),
    (re.compile(r'zo\'n'), 'zo een'),
    (re.compile(r'\'tis'), 'het is'),
    (re.compile(r'[ ]*\.\.\.[ ]*'), ' '),
    (re.compile(r'\!\?'), '?'),
    (re.compile(r'\?\!'), '?'),
    (re.compile(r'\!+'), '!'),
    (re.compile(r'\?+'), '?'),
    (re.compile(r'  +'), ' '),
    # en
    (re.compile(r'it\'s'), 'it is'),
    (re.compile(r'that\'s'), 'that is'),
    (re.compile(r'what\'s'), 'what is'),
    (re.compile(r'there\'s'), 'there is'),
    (re.compile(r'here\'s'), 'here is'),
    (re.compile(r'where\'s'), 'where is'),
    (re.compile(r'how\'s'), 'how is'),
    (re.compile(r'who\'s'), 'who is'),
    (re.compile(r'she\'s'), 'she is'),
    (re.compile(r'he\'s'), 'he is'),
    (re.compile(r'name\'s'), 'name is'),
    (re.compile(r'let\'s'), 'let us'),
    (re.compile(r'I\'m'), 'I am'),
    (re.compile(r'I\'ll'), 'I will'),
    (re.compile(r'I\'d'), 'I would'),
    (re.compile(r'I\'ve'), 'I have'),
    (re.compile(r'you\'re'), 'you are'),
    (re.compile(r'you\'ll'), 'you will'),
    (re.compile(r'you\'d'), 'you would'),
    (re.compile(r'you\'ve'), 'you have'),
    (re.compile(r'we\'re'), 'we are'),
    (re.compile(r'we\'ll'), 'we will'),
    (re.compile(r'we\'d'), 'we would'),
    (re.compile(r'we\'ve'), 'we have'),
    (re.compile(r'they\'re'), 'they are'),
    (re.compile(r'they\'ll'), 'they will'),
    (re.compile(r'they\'d'), 'they would'),
    (re.compile(r'they\'ve'), 'they have'),
    (re.compile(r'ain\'t'), 'am not'),
    (re.compile(r'isn\'t'), 'is not'),
    (re.compile(r'aren\'t'), 'are not'),
    (re.compile(r'wasn\'t'), 'was not'),
    (re.compile(r'weren\'t'), 'were not'),
    (re.compile(r'haven\'t'), 'have not'),
    (re.compile(r'hasn\'t'), 'has not'),
    (re.compile(r'hadn\'t'), 'had not'),
    (re.compile(r'won\'t'), 'will not'),
    (re.compile(r'wouldn\'t'), 'would not'),
    (re.compile(r'don\'t'), 'do not'),
    (re.compile(r'doesn\'t'), 'does not'),
    (re.compile(r'didn\'t'), 'did not'),
    (re.compile(r'can\'t'), 'can not'),
    (re.compile(r'couldn\'t'), 'could not'),
    (re.compile(r'shouldn\'t'), 'should not'),
    (re.compile(r'mightn\'t'), 'might not'),
    (re.compile(r'mustn\'t'), 'must not'),
    (re.compile(r'would\'ve'), 'would have'),
    (re.compile(r'should\'ve'), 'should have'),
    (re.compile(r'could\'ve'), 'could have'),
    (re.compile(r'might\'ve'), 'might have'),
    (re.compile(r'must\'ve'), 'must have'),
]


normalizations_token_patterns = [
    (re.compile(r'hé+'), 'he'),
    (re.compile(r'h[eé]+y'), 'he'),
    (re.compile(r'hm+'), 'hmm'),
    (re.compile(r'e+h+m+'), 'uh'),
    (re.compile(r'^ff$'), 'even'),
]

accent_map = str.maketrans({
    'á': 'a', 'à': 'a', 'ä': 'a',
    'é': 'e', 'è': 'e', 'ë': 'e',
    'í': 'i', 'ì': 'i', 'ï': 'i',
    'ó': 'o', 'ò': 'o', 'ö': 'o',
    'ú': 'u', 'ù': 'u', 'ü': 'u',
})

def normalize_text(text):
    text = text.lower()

    for pattern, replacement in normalizations_text_patterns:
        text = pattern.sub(replacement, text)

    text = text.translate(accent_map)

    return text


def normalize_tokens(tokens):
    new_tokens = []
    for token in tokens:
        for pattern, replacement in normalizations_token_patterns:
            token = pattern.sub(replacement, token)
        new_tokens.append(token)
    return new_tokens


class LegacyTextBlock:
    # Opcodes for raw text (using unused values)
    RAW_TEXT = 0xff

    def __init__(self, value):

        if isinstance(value, bytes):
          self.data = value
        if isinstance(value, str):
          self.text = value

        self.dicts = []

        paths = [
            'dictionaries/nl/_chatdict_tweebyte_woorden_engels',
            'dictionaries/nl/_chatdict_tweebyte_woorden'
            ]

        for path in paths:
            words = {}
            word_list = []
            with open(path, 'r', encoding='utf-8') as f:
                for i, w in enumerate(f.read().split()):
                    w = w.strip().lower()
                    words[w] = i
                    word_list.append(w)
            self.dicts.append((words, word_list))

    def encode(self):
        text = normalize_text(self.text)
        
        tokens = text.split()
        tokens = normalize_tokens(tokens)
        
        buf = bytearray()
        curr_dict = None
        curr_indexes = []
        curr_raw = []
        
        def flush_dict():

            if curr_indexes:
                
                if len(curr_indexes) >= 2:
                    buf.append(curr_dict * 2 + 1)
                    for i in curr_indexes:
                        buf.extend(i.to_bytes(2))
                    buf.extend([0, 0])
                
                else:
                    for i in curr_indexes:
                        buf.append(curr_dict * 2)
                        buf.extend(i.to_bytes(2))

        def flush_raw():
            if curr_raw:
                raw_text = ' '.join(curr_raw).encode('utf-8')
                buf.append(self.RAW_TEXT)
                buf.extend(len(raw_text).to_bytes(1))
                buf.extend(raw_text)

        for token in tokens:

            # Try dictionaries first
            found = False
            for dict_id in (1, 0):
                if token in self.dicts[dict_id][0]:

                    # If we have raw words pending, flush them first
                    if curr_raw:
                        flush_raw()
                        curr_raw = []
                    
                    if curr_dict != dict_id and curr_indexes:
                        flush_dict()
                        curr_indexes = []

                    curr_dict = dict_id
                    curr_indexes.append(self.dicts[dict_id][0][token])
                    found = True
                    break
            
            if not found:
                # If we have dictionary words pending, flush them first
                if curr_indexes:
                    flush_dict()
                    curr_indexes = []
                curr_raw.append(token)

        # Flush any remaining tokens
        if curr_indexes:
            flush_dict()
        if curr_raw:
            flush_raw()

        output = bytes(buf)
        return TEXT_BLOCK_LEGACY.to_bytes(1) + len(output).to_bytes(1) + output

    def decode(self):
        data = self.data
        tokens = []
        i = 0
        while i < len(data):
            opcode = data[i]
            i += 1
            
            if opcode == self.RAW_TEXT:
                length = data[i]
                i += 1

                raw_text = data[i:i + length].decode('utf-8')
                tokens.extend(raw_text.split())
                i += length

            else:
                dict_id      = opcode >> 1
                is_stream    = opcode & 1
                current_dict = self.dicts[dict_id]
    
                if is_stream:

                    while i < len(data) - 1:
                        idx = int.from_bytes(data[i:i+2])
                        if idx == 0:
                            i += 2
                            break
                        tokens.append(current_dict[1][idx])
                        i += 2
                else:
                    idx = int.from_bytes(data[i:i+2])
                    tokens.append(current_dict[1][idx])
                    i += 2

        return ' '.join(tokens)