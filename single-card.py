import json
import requests
from card import Card


""" url = 'https://yugioh.wikia.com/api.php?format=json&action=query&pageids=30438&prop=revisions&rvprop=content'

all_cards = json.load(open('yugioh-cards.json'))
card = requests.get(url).text
data = json.loads(card)
f = open(str(all_cards[0].get('id')) + '.json', 'w')
json.dump(data, f, indent=2) """

id = "30438"

card = json.load(open('30438.json'))
content = str(card.get('query').get('pages').get(id).get('revisions')[0].get('*')).split("\n")

card = Card()
set_found = False

NOT_SEARCH = ['ocg', 'adv', 'trad', 'sets', 'archseries']

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

f = open('30438-content.json', 'w')
dict = card.__dict__
dict['sets'] = card.sets
json.dump([dict], f, indent=2)