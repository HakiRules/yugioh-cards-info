class Card(object):
  es_name = ""
  es_lore = ""
  en_name = ""
  en_lore = ""
  image = ""
  card_type = ""
  property = ""
  effect_types = ""
  ocg = ""
  adv = ""
  trad = ""
  sets = []
  archseries = ""
  counter = ""
  action = ""
  database_id = ""

  def __setitem__(self, key, value):
    setattr(self, key, value)

  def __getitem__(self, key):
    return getattr(self, key)