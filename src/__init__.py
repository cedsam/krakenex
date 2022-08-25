def main():
    import krakenex
    import os
    from modules import keyFile
    from modules import mail
    import logging
    import keyring

    #configuration journaux
    os.remove('krakenapi.log')
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='krakenapi.log', encoding='utf-8', level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    
    #configuration mail
    smtpUser = keyring.get_password('orange.username', 'username')
    smtpPassword = keyring.get_password('smtp.orange.fr', 'password')
    smtpServer = 'smtp.orange.fr'
    smtpPort = 587
    destination = keyring.get_password('imap.gmail.com', 'username')

    #appel de l'api via krakenex
    kraken = krakenex.API()
    logging.info(kraken)

    #chargement clé privé et clé api dans windows (https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker)
    api_key = keyring.get_password('API_KEY_KRAKEN', 'KEY')
    api_sec = keyring.get_password('API_SEC_KRAKEN','SEC')
    keys = keyFile(api_key,api_sec)
    kraken.load_key(keys)

    #récuperation du solde
    try:
        soldeEuro = kraken.query_private("Balance")
    except:
        logging.warning("vérifier la connexion ou les clés API")
        subject='Krakenapi warning'
        msg='vérifier la connexion ou les clés API\nAdresse journaux :'
        mail (smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination)
        exit(1)
    soldeEuro = soldeEuro['result']
    soldeEuro = soldeEuro['ZEUR']

if __name__ == "__main__":
    main()