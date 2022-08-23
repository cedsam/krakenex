import krakenex
import os

#appel de l'api via krakenex
kraken = krakenex.API()

#chargement clé privé et clé api
api_key = os.environ['API_KEY_KRAKEN']
api_sec = os.environ['API_SEC_KRAKEN']
tmp = os.environ['TMP']
with open(tmp+'\\keys', "w") as f:
    f.write(api_key+"\n"+api_sec)
kraken.load_key(tmp+'\\keys')
os.remove(tmp+'\\keys')