from email   import message_from_bytes
from imaplib import IMAP4_SSL

import httpx

class IMAP:
    def __init__(self, email: str, password: str, ssl_url: str) -> None:
        self.imap = IMAP4_SSL(ssl_url)
        print(self.imap.login(email, password)) 
            
    def getLink(self) -> str:
        self.imap.select("Inbox")
        
        _, data = self.imap.search(None, 'ALL')
        print(data)

        for num in data[0].split():
            _, data = self.imap.fetch(num, '(RFC822)')
            rs_message = data[0][1]
            email_message = message_from_bytes(rs_message)
            email_body = ''
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        email_body += part.get_payload(decode=True).decode()
            else:
                email_body = email_message.get_payload(decode=True).decode()

            out = email_body
            spl = "https://click.discord.com/ls/click?upn="
            
            split = out.split(spl)
            
            if split != []:
                link = split[1]
                link = "https://click.discord.com/ls/click?upn=" + link 
                
                return link.replace(" ", "").replace("\r\n\r\n", "")

        return

class Kopeechka:
    def __init__(self, key: str) -> None:
        self.key = key
        self.balance = self.getBalance()
        
        if not self.balance:
            Exception("Invalid key")
    
    def getBalance(self):
        url = f"http://api.kopeechka.store/user-balance?token={self.key}&type=json&api=2.0"
        
        req = httpx.get(url)
        try:
            js = req.json()
        except:
            return
        
        if js.get("status") == "OK":
            return js.get("balance")
        else:
            return 
    
    def getMail(self):
        url = f"http://api.kopeechka.store/mailbox-get-email?site=discord.com&mail_type=OUTLOOK&token={self.key}&sender=discord&regex=&api=2.0"
        
        req = httpx.get(url)
        try:
            js = req.json()
        except:
            return
        
        if js.get("status") == "OK":
            return js
        else:
            return
    
    def checkMailbox(self, id: str):
        url = f"http://api.kopeechka.store/mailbox-get-message?full=1&spa=1&id={id}&token={self.key}&api=2.0"
        
        req = httpx.get(url)
        try:
            js = req.json()
        except:
            return
        
        if js.get("status") == "OK":
            return js.get("value")
        else:
            return
    
    def deleteMail(self, id: str):
        url = f"http://api.kopeechka.store/mailbox-delete-message?id={id}&token={self.key}&api=2.0"
        
        req = httpx.get(url)
        try:
            js = req.json()
        except:
            return
        
        if js.get("status") == "OK":
            return True
        else:
            return False
    