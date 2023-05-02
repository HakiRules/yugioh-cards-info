import requests
import json

url = 'https://yugioh.fandom.com/api/v1/Articles/List?category=TCG_cards&limit=9999999&namespaces=0'
cards = []
last_offset = ''

def get_card_page(offset=''):
  global last_offset

  json_text = json.loads(requests.get(url if offset == '' else url + '&offset=' + offset).text)
  last_offset = json_text.get('offset')
  return json_text['items']

cards += get_card_page()

while last_offset != None:
  cards += get_card_page(last_offset)
else:
  f = open('yugioh-cards.json', 'w')
  json.dump(cards, f, indent=2)
  print("Finished retrieving the cards!!")
  print("Total number of cards " + str(len(cards)))