def mail(smtpUser,smtpPassword,smtpServer,smtpPort,subject,msg,destination):
    import smtplib
    from email.message import EmailMessage

    mail = EmailMessage()
    mail.set_content(msg)
    mail['Subject'] = subject
    mail['From'] = smtpUser
    mail['To'] = destination

    with smtplib.SMTP(smtpServer, smtpPort) as smtp:
        smtp.set_debuglevel(1)
        smtp.starttls()
        smtp.login(smtpUser, smtpPassword)
        smtp.send_message(mail)

def keyFile(api_key,api_sec):
    import os
    tmp = os.environ['TMP']
    try:
        os.remove(tmp+'\\keys')
    except OSError:
        pass
    with open(tmp+'\\keys', "w") as f:
        f.write(api_key+"\n"+api_sec)
    return (tmp+"\keys")