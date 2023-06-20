import requests
import json
from card import Card
import numpy as np

url = 'https://yugioh.fandom.com/api/v1/Articles/List?category=TCG_cards&limit=9999999&namespaces=0'
cards = []
cards_content = []
last_offset = ''

def get_card_page(offset=''):
  global last_offset

  json_text = json.loads(requests.get(url if offset == '' else url + '&offset=' + offset).text)
  last_offset = json_text.get('offset')
  list = []
  for item in json_text['items']:
    list.append(str(item.get('id')))
  return list

def get_cards_by_ids(ids):
  NOT_SEARCH = ['ocg', 'adv', 'trad', 'sets', 'archseries']
  print(ids)
  ids_url = "|".join(ids)

  url = 'https://yugioh.wikia.com/api.php?format=json&action=query&pageids=' + ids_url +'&prop=revisions&rvprop=content'
  url_text = requests.get(url).text
  data = json.loads(url_text)

  all_cards = []

  for id in ids:
    content = str(data.get('query').get('pages').get(id).get('revisions')[0].get('*')).split("\n")

    card = Card()
    set_found = False

    for line in content:
        index = line.find('=') + 2

        # Find simple attributes inside line
        attributes = dir(Card)
        for attr in attributes:
          if line.__contains__(attr) and attr not in NOT_SEARCH:
              card[attr] = line[index:]

        if line.__contains__('| ocg'):
            card.ocg = line[index:]
        if line.__contains__('| adv'):
            card.adv = line[index:]
        if line.__contains__('| trad'):
            card.trad = line[index:]
        if set_found:
            if(line.__contains__("}}")):
                set_found = False
            else:
              card.sets.append(line[0:])
        if line.__contains__('related_to_archseries'):
            card.archseries = line[index:]
        if not set_found: set_found = line.__contains__('Card set|lang=en')

    card_dict = card.__dict__
    card_dict['sets'] = card.sets
    all_cards.append(card_dict)
  return all_cards
cards += get_card_page()

while last_offset != None:
  cards += get_card_page(last_offset)
else:
  try:
    sections = cards.__len__() / 25
    splitted_cards = np.array_split(cards, sections)
    for card_ids in splitted_cards:
      print
      cards_content += get_cards_by_ids(card_ids)
  except:
     print(f"error on section {card_ids}")
  finally:
    f = open('yugioh-cards-content.json', 'w')
    json.dump(cards_content, f, indent=2)
    print("Finished retrieving the cards!!")
    print("Total number of cards " + str(len(cards)))