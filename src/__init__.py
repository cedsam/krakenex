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
    smtpPassword = keyring.get_password('orange.password', 'password')
    smtpServer = 'smtp.orange.fr'
    smtpPort = 587
    destination = keyring.get_password('gmail.username', 'username')

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
        msg='vérifier la connexion ou les clés API\nAdresse journaux :'
        logging.warning("{msg}")
        subject='Krakenapi warning'
        mail (smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination)
        exit(1)
    soldeEuro = soldeEuro['result']
    soldeEuro = float (soldeEuro['ZEUR'])

    #vérification du solde
    solde = float(args.p)
    solde = soldeEuro - solde
    if solde < 0:
        msg='le solde est insuffisant, procéder à un virement de fonds (btc, eur...)'
        logging.warning("{msg}")
        subject='Krakenapi warning'
        mail (smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination)
        exit(1)

if __name__ == "__main__":
    #ajout prix d'achat
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-put", "--p", required=True, type=int, help="prix d'achat")
    parser.add_argument("-asset", "--a", required=True, type=str, help="actif a acheter")
    args = parser.parse_args()

    main()