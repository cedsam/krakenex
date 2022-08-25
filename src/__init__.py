def main():
    import krakenex
    import os
    from modules import keyFile
    #appel de l'api via krakenex
    kraken = krakenex.API()
    
    #chargement clé privé et clé api
    api_key = os.environ['API_KEY_KRAKEN']
    api_sec = os.environ['API_SEC_KRAKEN']
    keys = keyFile(api_key,api_sec)
    kraken.load_key(keys)
    #récuperation du solde
    soldeEuro = kraken.query_private("Balance")
    soldeEuro = soldeEuro['result']
    soldeEuro = soldeEuro['ZEUR']

if __name__ == "__main__":
    main()