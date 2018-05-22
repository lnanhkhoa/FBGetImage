import smtplib

# sender = 'lnanhkhoa303@gmail.com'
# receivers = ['lnanhkhoa.tk@gmail.com']
#
message = "\r\n".join(["""From: From Person <lnanhkhoa303@gmail.com>
To: To Person <lnanhkhoa.tk@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""])
#
# try:
#    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
#    smtpObj.ehlo()
#    smtpObj.starttls()
#    smtpObj.sendmail(sender, receivers, message)
#    print ("Successfully sent email")
# except smtplib.SMTPException:
#    print ("Error: unable to send email")



def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


# SMTP_SSL Example
gmail_user = "lnanhkhoa303@gmail.com"
gmail_pwd = "lnak121104"
server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server_ssl.ehlo() # optional, called by login()
server_ssl.login(gmail_user, gmail_pwd)
# ssl server doesn't support or need tls, so don't call server_ssl.starttls()
server_ssl.sendmail(gmail_user, 'lnanhkhoa.tk@gmail.com', message)
#server_ssl.quit()
server_ssl.close()
print('successfully sent the mail')