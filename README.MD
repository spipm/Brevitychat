# Chatspreek protocol

Creates compressed small text messages from static dicts and data types.

## Frame format

header
  byte 1: [4 bit version      | 4 bit language]
  byte 2: [4 bit compression  | 4 bit reserved]
payload
  [block type][block data]
  [block type][block data]
  ..
  [block type][block data]

## Optcode mapping

0x00            LINE_END

0x11            GPS_BLOCK_4
0x12            GPS_BLOCK_5
0x13            GPS_BLOCK_6
0x14            GPS_BLOCK_7
0x15            DATE_BLOCK
0x16            NUMBER_BLOCK
0x17            LINK_BLOCK
0x18            TEXT_BLOCK_LEGACY
0x19            TEXT_BLOCK

0x31            SOS
0x32            REQ
0x33            ACK
0x34            WARN
0x35            INFO
0x36            CMD

0x41            MARKERS
0x42            MEME

## Block examples

- SOS (Noodoproepen)

    SOS | Medisch | 52.0907,5.1214 | Bloeding
    SOS | Brand | 52.3676,4.9041 | Huis in vuur

- REQ (Verzoeken om Hulp/Informatie)

    REQ | Water | 52.0907,5.1214
    REQ | EH-kit | Verzamelpunt
    REQ | Type Hulp | Locatie | Details
    REQ | Voedsel | Verzamelpunt | Pizza nodig
    REQ | Are you busy? 
    REQ | Have you anything for me? 
    REQ | Are you ready? 
    REQ | Have you news of ____ (call sign)? 
    REQ | What is your estimated time of arrival at ____ (or over ____) (place)? 

- ACK (Bevestigingen)

    ACK | Bericht ontvangen
    ACK | Hulp onderweg

- WARN

    WARN | Vijanden gespot | Coordinaten
    WARN | Large force of indeterminate numbers and formation.

- INFO (Informatieoverdracht)

    INFO | Weg afgesloten | A12
    INFO | Veilige route naar | via N11
    INFO | Veilig
    INFO | Onderweg naar verzamelpunt
    INFO | To act independently or according to instruction

- CMD (Instructies en Bevelen)

    CMD | Beweeg naar verzamelpunt | 52.3676,4.9041
    CMD | Controleer op slachtoffers | 52.3676,4.9041

- MARKER

    MARKER | zelf
    MARKER | enemy
    MARKER | friend
    MARKER | neutral
    MARKER | verzamelpunt
    MARKER | feest
    MARKER | verblijf
    MARKER | materiaal
    MARKER | voorraad
    MARKER | start
    MARKER | end / expire

## Future stuff

- AUTH
    
    AUTH | Key exchange
    
- DEBUG
    
    Examples
    DEBUG | com test | reply x
    DEBUG | auth challenge | encrypt x
    DEBUG | auth challenge | recall x
    DEBUG | Unsupported version

- NEG > Onderhandel
- SYS
- context ID
  - ID gekoppeld aan een event
- referentie naar eerder bericht
    REF | Frame ID | Msg num
- memes from images
- temp value
    - optie om waarde tijdelijk op te slaan
    - optie om waarde terug te halen
    Voorbeeld: [INFO][FEEST][START][TMP1][0][INFO][Verzamelpunt][TMP1]

### Data Type blocks

- GPS coordinaten
- datum/tijd in timestamp
- link
- nummer
- text / raw text

## Text blocks

Created a custom text block compressor only to find out that this exists:
https://github.com/siara-cc/Unishox2

Ran tests and this seems to work slightly better than my custom text block compressor, so I added this as a dependancy

Found that while browsing the source code that Unishox2 is used
  Will the binary protocol now worsen the compression?
  -> tests say no
  -> Using (serialized) plaintext might provide better compression

## Encryption

In Meshtastic, messages are encrypted to channels with an AES PSK, and messages are encrypted in DMs with pub crypto by default. 

 -> so we only need encryption if we want to encrypt for a specfic node on a public channel
 https://python.meshtastic.org/mesh_interface.html#meshtastic.mesh_interface.MeshInterface.showNodes
 -> currently not really a use case because users can set a custom channel in the lora node
 -> if needed it can be added with a wrapper

## URLs

First I wanted to encode only a tinyurl code, but this would compromise privacy too much and this application doesn't want to be internet dependant.

```
Method          Avg Time (s)    Avg Size (bytes)
--------------------------------------------------
base64+zlib     0.000016        73
base64+lzma     0.001095        122
base85+zlib     0.000014        69
base85          0.000004        61
base122         0.000013        56
zlib            0.000005        55
lzma            0.000954        106
base122+zlib    0.000020        64
base122+lzma    0.000957        113
```

Plain zlib seems to be the best option for encoding urls. urls are annoying because they can be considered arbitrary byte sequences, which is not optimal for what we're trying to achieve with this protocol.

## Sources

English dict taken from cmix.

https://raw.githubusercontent.com/byronknoll/cmix/refs/heads/master/dictionary/english.dic