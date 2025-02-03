
# Test compression rates against chat-gpt generated chat messages

# TextBlock vs zlib and unishox2 (TextBlock is lossy)
# Average compression rate of texts sample_texts_rough TextBlock
# 4.79%
# Average compression rate of texts sample_texts_rough zlib
# -30.04%
# Average compression rate of texts sample_texts_rough unishox2
# 20.73%
# Average compression rate of texts sample_texts_clean TextBlock
# 30.37%
# Average compression rate of texts sample_texts_clean zlib
# 11.41%
# Average compression rate of texts sample_texts_clean unishox2
# 38.64%
# -> better for < 255 byte messages, but zlib gets better when messages get bigger

# TextBlock vs zlib and unishox2 (TextBlock is lossy) + unishox2 (because meshtastic uses unishox2)
# Average compression rate of texts sample_texts_rough TextBlock
# -4.75%
# Average compression rate of texts sample_texts_rough zlib
# -43.46%
# Average compression rate of texts sample_texts_rough unishox2
# 6.79%
# Average compression rate of texts sample_texts_clean TextBlock
# 27.33%
# Average compression rate of texts sample_texts_clean zlib
# 1.12%
# Average compression rate of texts sample_texts_clean unishox2
# 30.85%


sample_texts_rough = [
    """Dit is een test bericht. Wat's er aan de hand?
    
    Dit is nog een blok, met enkele samengestelde-woorden.""",
    "Hallo wereld!",
    "Hoi daar. Hoe gaat het?",
    "Wat's er? 't Is een mooie dag!",
    "Hallo, wereld! Dit is een test-bericht.",
    "Eerste paragraaf.\n\nTweede paragraaf.",
    "",
    "   ",
    "a"*255,
    "Bel me op 123-456-7890! E-mail: test@voorbeeld.nl",
    "Hallo! 👋 Hoe gaat het? 🙂",
    "Wauw!!! Dit is geweldig...",
    'Hij zei "Hallo" en vertrok.',
    "Dit    heeft    meerdere    spaties.",
    "Bezoek https://voorbeeld.nl/pagina?id=123",
    "Jan's boek is er niet.",
    "Hallo (wereld)!",
    "HaLLo WeRELD!",
    "Hallo\twereld!\nNieuwe\tregel.",
    "Eerste regel!\n\n\nTweede regel.",
        "Hoe gaat ‘t? 🤔 of... niet?",
    "Ehm... wat was het ook alweer!? 🤷‍♂️",
    "Serieus...?! Wéér dat probleem? #fail",
    "Dus—wacht even—wat bedoel je?",
    "Hallo??? Ben je daar—of niet!?",
    "Als je komt (toch?), laat je ‘t ff weten...",
    "“Gisteren zei je: ‘dat fixen we wel’, toch?”",
    "...en toen gebeurde er dus helemaal NIETS!?",
    "Waarom werkt ‘t—of werkt ’t juist niet?!?",
    "Wat!? 🤯 Dit kan toch niet waar zijn—of wel?",
    "Oké... maar wáár ben je nu!?! 😅",
    "Hm. Misschien... toch beter om ff te bellen?",
    "W8 ff—je zei eerder iets ánders, weet je nog!?",
    "Dus... wat nu? #geenidee 😬",
    "Hé! (of moet ik zeggen: HÉÉÉ!!!) 🤣",
    "OMG—dat is ZO raar—letterlijk!!",
    "Wat. Een. Drama. (Echt hoor 🙄).",
    "En toen ineens... 💥 alles kapot.",
    "Kun je dat fixen...? (of juist niét...?)",
    "Gisteren—of was het eergisteren?? Ik weet ‘t niet meer...",
    "Kom je mee—of moet ik alleen? (Laat ff weten.)",
    "Fix dit! NU!!! 🚨 (of asap, pls...)",
    "Oke... “dat was dus niet echt handig,” zei hij 🙃",
    "Dus... hoe lang gaat dit duren?!? (Echt waar!)",
    "Waarom—ik herhaal: WAAROM—is dit zo moeilijk!?",
    "Oké, maar: hoezo werkt ’t niet “meer”?! 🤔",
    "Serieus, hoe kan DIT gebeuren—altijd, trouwens?!?",
    "Hé? Je zei toch dat ’t werkte... of niet?!",
    "En toen: *poef!* Alles weg. Wát nu!?",
    "“Wat doe je?!?!” vroeg ik. En toen... stilte.",
    "Wat betekent dit: ‘geen idee’... echt NIEMAND weet het?",
    "Ah... dus “dat” is het probleem. Begrijp ik ’t goed?!",
    "Laat ff weten wanneer je er bent... (of stuur een 🏠 emoji).",
    "Wáár was je trouwens—ik zocht je!? 😅",
    "Check je telefoon!!! NU!! 📱",
    "Dus. Punt. Nu. (Snap je wat ik bedoel?)",
    "Wtf?!?! (Maar echt, WAT IS DIT.)",
    "Hééé... ff serieus: wat gebeurde daar net?? 🤯",
    "Waar—en ik bedoel WAAR—is die info gebleven?!",
    "Ja nee, ‘t is oké... of... nee? Laat maar.",
    "Omg... echt... “hilarisch”... of NIET grappig??",
    "“Even eerlijk: dit kan niet, toch?” dacht ik.",
    "Zeg maar: wat nu? *insert paniek hier*",
    "Dus dit is het plan?—OF NIET? #verwarring",
    "Waarom!!! Is!!! Dit!!! Zo!!! Moeilijk!!! 😭",
    "... en toen zei hij: “komt goed”... (maar niet dus).",
    "Dus: ga je mee, of blijf je staan, of—?",
    "Hééé, ik snap ’t niet... leg je dit ff uit?",
    "Alles goed? (Of niet?? Zeg ’t eerlijk!)"
]
sample_texts_clean = [
    "Hoe gaat het met je? Het is al een tijdje geleden dat we hebben gesproken. Zullen we binnenkort even afspreken?",
    "Ik ben onderweg, maar het verkeer is echt vreselijk. Ik laat je weten zodra ik er bijna ben.",
    "Heb je vanavond tijd? We kunnen misschien even iets drinken of een serie kijken. Laat maar weten wat je denkt!",
    "Wat ben je allemaal aan het doen vandaag? Ik heb het redelijk druk, maar kan misschien later op de dag wat tijd vrijmaken.",
    "Alles goed daar? Hier is het nogal chaotisch, maar ik probeer mijn dag een beetje rustig te houden.",
    "Wat zullen we eten vanavond? Ik heb wel zin in iets makkelijks. Misschien bestellen we pizza of maken we pasta?",
    "Stuur me even je locatie als je er bent. Dan weet ik zeker dat ik op de juiste plek ben.",
    "Bedankt voor je hulp eerder! Zonder jou had ik het echt niet gered. We moeten snel iets terugdoen voor je.",
    "Heb je dat artikel gelezen waar ik het over had? Het is echt interessant, en ik ben benieuwd naar wat jij ervan vindt.",
    "Ik moet je even spreken over iets belangrijks. Heb je later tijd voor een korte call?",
    "Wat een lange dag, zeg. Ik ben blij dat ik nu eindelijk thuis ben. Wat doe jij vanavond?",
    "Ben je al onderweg? Laat me even weten hoe laat je hier denkt te zijn, dan kan ik het een beetje plannen.",
    "Heb je vandaag iets spannends gedaan? Bij mij was het een beetje saai, maar misschien heb jij een leuk verhaal.",
    "Zullen we morgen ergens koffie drinken? Het is alweer zo lang geleden dat we elkaar hebben gezien.",
    "Het is hier echt slecht weer. Hoe is het bij jou? Ik hoop dat het niet al te erg is als je naar buiten moet.",
    "Heb je nog hulp nodig met dat project waar je mee bezig was? Laat maar weten, ik help graag.",
    "Ik zit te denken aan een dagje weg dit weekend. Heb je zin om mee te gaan? Misschien kunnen we ergens wandelen.",
    "Sorry dat ik nog niet had gereageerd. Het is een beetje druk geweest hier, maar hoe gaat het met jou?",
    "Ik had net zo’n grappig moment! Ik moet het je echt vertellen als we elkaar zien.",
    "Alles is geregeld voor vanavond. Laat even weten of je iets extra’s nodig hebt, dan neem ik het mee.",
    "Ik zag net dat ding waar we het laatst over hadden. Het is precies wat we nodig hebben. Zullen we het bestellen?",
    "Hoe is het op je werk? Het lijkt me echt lastig wat je daar allemaal moet doen, maar je kan het zeker aan!",
    "Heb je al plannen voor het weekend? Ik zat te denken om misschien iets samen te doen als je tijd hebt.",
    "Wat een rare dag vandaag. Ik had echt verwacht dat het rustiger zou zijn, maar het lijkt alsof alles tegelijk komt.",
    "Wanneer komt die serie nou eindelijk uit? Ik kan echt niet wachten om het te gaan kijken.",
    "Sorry dat ik te laat ben. Het verkeer zat niet mee, maar ik ben er over een paar minuten!",
    "Laat maar weten wanneer je tijd hebt. Ik pas me wel aan aan jouw schema.",
    "Ik zit net te denken dat we al heel lang geen spelletjesavond meer hebben gehad. Zullen we dat snel weer doen?",
    "Hoe voel je je vandaag? Je klonk laatst een beetje moe, dus ik hoop dat je wat beter hebt geslapen.",
    "Bedankt voor je bericht! Ik kom zo terug op wat je zei, want ik wil het goed doornemen.",
    "Wat een grappige foto die je stuurde! Heb je die zelf gemaakt? Het ziet er echt geweldig uit."
]

from classes.TextBlock import TextBlock
import zlib
import base64

import unishox2


def gen_average_compression_rate(texts, compression_function):

  compressed_lenghts = []
  for text in texts:
    if len(text) > 250 or len(text) == 0:
      continue
    encoded = compression_function(text)

    # but then unishox2 happens
    # encoded = base64.b64encode(encoded)
    encoded = unishox2.compress(encoded)[0]
    
    compressed_lenghts.append(100-((len(encoded)/len(text))*100))

  average_compression_rate = sum(compressed_lenghts) / len(compressed_lenghts)
  return average_compression_rate

print("Average compression rate of texts sample_texts_rough TextBlock")
average_compression_rate = gen_average_compression_rate(sample_texts_rough, lambda x: TextBlock(x).encode())
print("%s%%" % round(average_compression_rate, 2))

print("Average compression rate of texts sample_texts_rough zlib")
average_compression_rate = gen_average_compression_rate(sample_texts_rough, lambda x: zlib.compress(x.encode()))
print("%s%%" % round(average_compression_rate, 2))

print("Average compression rate of texts sample_texts_rough unishox2")
average_compression_rate = gen_average_compression_rate(sample_texts_rough, lambda x: unishox2.compress(x)[0])
print("%s%%" % round(average_compression_rate, 2))

print("Average compression rate of texts sample_texts_clean TextBlock")
average_compression_rate = gen_average_compression_rate(sample_texts_clean, lambda x: TextBlock(x).encode())
print("%s%%" % round(average_compression_rate, 2))

print("Average compression rate of texts sample_texts_clean zlib")
average_compression_rate = gen_average_compression_rate(sample_texts_clean, lambda x: zlib.compress(x.encode()))
print("%s%%" % round(average_compression_rate, 2))

print("Average compression rate of texts sample_texts_clean unishox2")
average_compression_rate = gen_average_compression_rate(sample_texts_clean, lambda x: unishox2.compress(x)[0])
print("%s%%" % round(average_compression_rate, 2))
