import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Message:

    def __init__(self, name, subject, date = None, template = None):

        self.name = name
        self.date = date
        self.Subject = subject

        if not template:
            body = self.default
        else:
            if not os.path.exists(template):
                raise OSError('Given path for template file does not exist.')
            with open(template) as f:
                body = f.read()

        self.__body = body
        self.validate_body()

        self.__msg = MIMEMultipart()

    def __str__(self):

        attributes = ['From', 'To', 'Subject']
        for attr in attributes:
            if hasattr(self, attr):
                self.__msg[attr] = getattr(self, attr)

        content = dict(name=self.name)
        if self.date:
            content.update(dict(date=self.date))

        self.__msg.attach(MIMEText(self.__body.format(**content)))

        return self.__msg.as_string()

    @property
    def default(self):
        pass

    def validate_body(self):
        pass

