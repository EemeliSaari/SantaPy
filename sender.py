import smtplib
import getpass


class Sender(smtplib.SMTP):

    PROVIDER_MAP = dict(
        gmail = ('smtp.gmail.com', 587)
    )

    def __init__(self, provider):
        super(Sender, self).__init__(*self.PROVIDER_MAP[provider])

    def __enter__(self):
        super(Sender, self).__enter__()

        self.starttls()
        self.login(*self.read_credentials())

        return self

    def read_credentials(self):
        email = input('Your email address: ')
        password = getpass.getpass('Your password: ')

        self.__email = email

        return email, password

    def sendmail(self, email_to, msg, mail_options = []):

        super(Sender, self).sendmail(self.__email, email_to, msg, mail_options)