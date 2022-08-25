def main():
    import krakenex
    import os
    from modules import keyFile
    import logging
    import keyring

    #configuration journaux
    os.remove('krakenapi.log')
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='krakenapi.log', encoding='utf-8', level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    
    #appel de l'api via krakenex
    kraken = krakenex.API()
    logging.info(kraken)

    ##chargement clé privé et clé api
    api_key = keyring.get_password('API_KEY_KRAKEN', 'KEY')
    api_sec = keyring.get_password('API_SEC_KRAKEN','SEC')
    keys = keyFile(api_key,api_sec)
    kraken.load_key(keys)

    #récuperation du solde
    soldeEuro = kraken.query_private("Balance")
    soldeEuro = soldeEuro['result']
    soldeEuro = soldeEuro['ZEUR']
if __name__ == "__main__":
    main()