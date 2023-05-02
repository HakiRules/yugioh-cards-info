import json
import requests

""" url = 'https://yugioh.wikia.com/api.php?format=json&action=query&pageids=30438&prop=revisions&rvprop=content'

all_cards = json.load(open('yugioh-cards.json'))
card = requests.get(url).text
data = json.loads(card)
f = open(str(all_cards[0].get('id')) + '.json', 'w')
json.dump(data, f, indent=2) """

card = json.load(open('30438.json'))
content = str(card.get('query').get('pages').get('30438').get('revisions')[0].get('*'))
content.find
f = open('30438-content.json', 'w')
json.dump(content, f, indent=2)