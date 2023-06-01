from base64 import b64encode
from httpx  import get
from numpy  import array
from os     import listdir, path as pth
from random import choice, choices
from json   import dumps, loads
from string import ascii_letters, digits

class Utils:
    def __init__(self) -> None:
        with open("config.json", "r") as f:
            self.config = loads(f.read())
            
            self.api = self.config["solving_service"]
            self.key = self.config["captcha_api_key"]
            
            self.email_verify = self.config["email_verify"]
            self.phone_verify = self.config["phone_verify"]
            
            if not self.email_verify:
                self.imap         = False
                self.imap_ssl_url = None
                
            self.imap         = self.config["imap"]
            self.imap_ssl_url = self.config["imap_ssl_url"]
            
            self.kopeechka_key = self.config["kopeechka_api_key"]
            
            self.api_type = self.config["sms_api"]
            if self.api_type == "onlinesim":
                self.onlinesim_key = self.config["onlinesim_api_key"]
            elif self.api_type == "vaksms":
                self.vaksms = self.config["vaksms_api_key"]
                
            
        with open("data/names.txt", "r", encoding="latin-1") as f:
            self.names = array(f.read().splitlines(), dtype="S")
        
        with open("data/bios.txt", "r", encoding="latin-1") as f:
            self.bios = array(f.read().splitlines(), dtype="S")
        
        with open("data/proxies.txt", "r", encoding="latin-1") as f:
            self.proxies = array(f.read().splitlines(), dtype="S")
        
        with open("data/emails.txt", "r") as f:
            self.emails = array(f.read().splitlines(), dtype="S")

        self.avatars = []

        for path in listdir("data/avatars/"):
            if pth.isfile(pth.join("data/avatars/", path)):
                self.avatars.append(path)
        
        self.avatars = array(self.avatars, dtype="S")
    
    def getBuildNum(self) -> int:
        js = get("https://discord.com/app").text.split('"></script><script src="/assets/')[2].split('" integrity')[0]
        req = get(
         f"https://discord.com/assets/{js}"
        )

        if req.status_code == 200:
            build_number = req.text.split('(t="')[1].split('")?t:"")')[0]

            return build_number
    
    def randomProxy(self) -> str:
        return choice(self.proxies).decode()
    
    def randomName(self) -> str:
        return choice(self.names).decode()
    
    def randomBio(self) -> str:
        return choice(self.bios).decode()

    def randomEmail(self) -> str:
        return choice(self.emails).decode().split(":")
    
    def randomPassword(self) -> str:
        return "".join(choices(ascii_letters + digits, k=12))
    
    def randomAvatar(self) -> bytes:
        with open(f"data/avatars/{choice(self.avatars).decode()}", "rb") as f:
            return f.read()
    
    def XSuperProperties(self, buildNum: int, chrome_version: str = "113"):
        return b64encode(dumps({"os":"Windows","browser":"Chrome","device":"","system_locale":"pl-PL","browser_user_agent":f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36","browser_version":f"{chrome_version}.0.0.0","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":buildNum,"client_event_source":None,"design_id":0}).encode()).decode()