from mailbox import Message
import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


class EMail:
    def __init__(self, login: str, password: str):
        """
        :param login: Authorization login for mail server
        :param password: Authorization password for mail server
        """
        self.gmail_smtp = "smtp.gmail.com" # Сервер исходящей почты
        self.gmail_imap = "imap.gmail.com" # Сервер входящей почты
        self.login : str = login # Login авторизации на сервере
        self.password : str = password # Password авторизации на сервере

    #send message
    def send_message(self, recipients: List[str], subject: str, message: str):
        """
        :param recipients: List of email recipients
        :param subject: Email subject
        :param message: Email message (text body)
        :return: None
        """
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        ms = smtplib.SMTP(self.gmail_smtp, 587) # identify ourselves to smtp gmail client
        ms.ehlo() # secure our email with tls encryption
        ms.starttls() # re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(msg['From'], msg['To'], msg.as_string())
        ms.quit() #send end
        
        #receive
    def receive_message(self, header: str) -> Message:
        """
        :param header: Subject for receiving email
        :return: Received email
        """
        mail = imaplib.IMAP4_SSL(self.gmail_imap)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else "ALL"
        result, data = mail.uid('search', '', criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, "(RFC822)")
        raw_email = data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        mail.logout() #end receive
        return email_message

if __name__ == '__main__':

    login_ = 'login@gmail.com'  # Login авторизации на сервере
    password_ = 'qwerty'  # Password авторизации на сервере
    subject_ = 'Subject'  # Тема отправляемого письма
    recipients_ = ['vasya@email.com', 'petya@email.com']  # Адреса получателей
    message_ = 'Message'  # Текст письма
    header_ = '' # Тема получаемого письма/писем, если '' - то получить все

    eml = EMail(login_, password_)
    eml.send_message(recipients_, subject_, message_)
    eml.receive_message(header_)