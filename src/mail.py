from email.message import EmailMessage

orangeUser = 'cedric.samardzija@orange.fr'
orangePassword = ''
mail = EmailMessage()
mail.set_content('Krakenapi info')
mail['Subject'] = 'Krakenapi (erreurs)'
mail['From'] = orangeUser
mail['To'] = 'cedric.samardzija@gmail.com'


with smtplib.SMTP("smtp.orange.fr", port=587) as smtp:
    smtp.set_debuglevel(1)
    smtp.starttls()
    smtp.login(orangeUser, orangePassword)
    smtp.send_message(mail)