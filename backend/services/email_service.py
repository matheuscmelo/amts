import smtplib, ssl, os

HOST = os.environ.get('HOST', 'localhost')
SMTP_SERVER = os.environ.get('SMTP_SERVER', "mail.lsd.ufcg.edu.br")
PORT = os.environ.get('SMTP_PORT', 587)
PASSWORD = os.environ.get('SMTP_PASSWORD')
SENT_FROM = os.environ.get('SMTP_SENT_FROM', "amts@lsd.ufcg.edu.br")
SMTP_USER = os.environ.get('SMTP_USER', "amts@lsd.ufcg.edu.br")



def send_password_reset_email(user, token):

    to = [user.email]
    subject = 'AMTS - Reset de senha'
    body = f'http://{HOST}/reset-password/{token}'
    email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s\n" % (SENT_FROM, ", ".join(to), subject, body)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(SMTP_USER, PASSWORD)
        server.sendmail(SENT_FROM, to, email_text)
        server.close()
