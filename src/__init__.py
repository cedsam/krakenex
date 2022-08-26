def main():
    import krakenex
    import os
    from modules import keyFile
    from modules import mail
    import logging
    import keyring
    import re

    #configuration journaux
    try:
        log = os.environ['TMP']+"\\krakenapi.log"
        os.remove(log)
    except:
        pass
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=log, encoding='utf-8', level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
    
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
    os.remove(keys)
    #récuperation du solde
    soldeEuro = kraken.query_private("Balance")
    if not 'result' in soldeEuro:
        msg='vérifier la connexion, les clés API ou la requête\n'
        logging.warning(msg)
        subject='Krakenapi warning'
        mail (smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination)
        exit(1)
    soldeEuro = float (soldeEuro['result']['ZEUR'])

    #vérification du solde
    solde = float(args.p)
    solde = soldeEuro - solde
    if solde < 0:
        msg='le solde est insuffisant, procéder à un virement de fonds (btc, eur...)'
        logging.warning(msg)
        subject='Krakenapi warning'
        mail (smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination)
        exit(1)

    #execution de l'ordre
    assetValue = kraken.query_public('Ticker?pair='+args.a)
    assetValue = float(args.p)/(float(assetValue['result'][args.a]['a'][0]))
    assetValue = str(assetValue)
    data = {'nonce': '0', 'ordertype' : 'market', 'type':'buy', 'volume': ''+assetValue+'', 'pair':''+args.a+'', 'validate' :'False'}
    assetValue = kraken.query_private("AddOrder",data)
    logging.info(assetValue)
    assetValue = str(assetValue)
    subject = 'Achat via Krakenapi'
    msg = 'un ordre est en cours\n(info : '+assetValue+')'
    mail (smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination)

if __name__ == "__main__":
    #ajout prix d'achat
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-put", "--p", required=True, type=float, help="prix d'achat")
    parser.add_argument("-asset", "--a", required=True, type=str, help="actif a acheter (voir liste Tradable Asset Pairs)")
    args = parser.parse_args()

    main()