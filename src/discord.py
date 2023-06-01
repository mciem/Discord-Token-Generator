from .client import Client
from random  import randint, choice
from base64  import b64encode
from json    import dumps
from time    import time, sleep

import websocket


class Discord:
    def __init__(self, proxy: str, xsup: str, utils: object, console: object, chrome_version: str): 
        self.token                = None
        self.unlocked             = None
        self.email_verified       = None
        self.phone_verified       = None
        self.flags                = None
        self.humanized            = [] 
        
        
        client       = Client(proxy, chrome_version)
        self.session = client.session
        self.headers = client.headers
        self.proxy   = client.proxy
        self.xsup    = xsup
        
        self.utils     = utils
        self.console   = console

    
    def generate(self, cap: str, name: str, invite: str):
        headers = self.headers
        headers["referer"] = "https://discord.com/"  
        
        req = self.session.get("https://discord.com/api/v9/experiments", proxy=self.proxy, headers=headers )
        resp = req.json()
        
        if resp.get("fingerprint"):
            fingerprint = resp["fingerprint"]
        else:
            self.console.error(f"Failed to get fingerprint")
            return
        
        headers["x-fingerprint"]      = fingerprint
        headers["x-super-properties"] = self.xsup

        payload = {
            "fingerprint" : fingerprint,
            "consent"     : True,
            "username"    : name,
            "captcha_key" : cap,
            "invite"      : None, #invite if invite != None else None,
        }
        
        #headers["content-length"] = str(len(dumps(payload)))
        
        req = self.session.post(f"https://discord.com/api/v9/auth/register", proxy=self.proxy, headers=headers, json=payload )
        match req.status_code:
            case 201:
                data = req.json()
                
                self.token = data["token"]
                
                check = self.checkToken()
                match check:
                    case 200:
                        self.checkFlags()
                        
                        self.unlocked = True
                    
                    case _:
                        self.unlocked = False

            case 400:
                self.token = "invalid captcha"
            
            case 429:
                sleep(5)
                self.generate(cap, name, invite)
                
            case _:
                self.token = f"unkown status code {str(req.status_code)}"
    
    def checkToken(self) -> int:
        headers                  = self.headers
        headers["authorization"] = self.token
        
        req = self.session.get(f"https://discord.com/api/v9/users/@me/settings", proxy=self.proxy, headers=headers)

        return req.status_code
    
    def checkFlags(self):
        headers                  = self.headers
        headers["authorization"] = self.token
                
        req = self.session.get(f"https://discord.com/api/v9/users/@me", proxy=self.proxy, headers=headers)
        data = req.json()

        flag = data.get("public_flags")
        if flag == 1048576:
            self.flags = "SPAMMER"
        else:
            self.flags = "NONE"
    
    def setBirthdate(self):
        headers = self.headers
        
        headers["authorization"]    = self.token

        payload = {
            "date-of-birth": f"{str(randint(1980,2000))}-{str(randint(1,12))}-{str(randint(1,28))}"
        }
        
        
        req = self.session.patch(f"https://discord.com/api/v9/users/@me", proxy=self.proxy, headers=headers, json=payload)
        
        if req.status_code == 200:
            self.humanized.append("birthdate")
        else:
            match req.status_code:
                case 401:
                    self.console.error(f"Failed to set bio -> token invalid")
                           
                case _:
                    self.console.error(f"Failed to set bio -> {req.status_code}")
    
    def setBio(self, bio: str):
        headers = self.headers
        
        headers["authorization"]    = self.token

        payload = {
            "bio": bio
        }
        
        req = self.session.patch(f"https://discord.com/api/v9/users/@me", proxy=self.proxy, headers=headers, json=payload) 
        
        if req.status_code == 200:
            self.humanized.append("bio")
        else:
            match req.status_code:
                case 401:
                    self.console.error(f"Failed to set bio -> token invalid")
                
                case _:
                    self.console.error(f"Failed to set bio -> {req.status_code}")
    
    def setAvatar(self, avatar: bytes):
        self.websocket()
        
        self.console.websocket(f"{self.token[:32]}****")
        
        headers = self.headers
        
        headers["authorization"]      = self.token
        headers["x-super-properties"] = self.xsup
        headers["referer"]            = "https://discord.com/channels/@me"
        
        av_enc = b64encode(avatar).decode("ascii")
        
        payload = {
            "avatar": f"data:image/png;base64,{av_enc}"
        }
        
        req = self.session.patch(f"https://discord.com/api/v9/users/@me", proxy=self.proxy, headers=headers, json=payload)

        if req.status_code == 200:
            self.humanized.append("avatar")
        else:
            match req.status_code:
                case 401:
                    self.console.error(f"Failed to set bio -> token invalid")

                case _:
                    self.console.error(f"Failed to set bio -> {req.status_code}")
    
    def websocket(self):
        ws = websocket.WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        ws.send(dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 8189,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "en-US",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    "browser_version": "113.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 199933,
                    "client_event_source": None,
                    "design_id": 0
                },
                "presence": {
                    "status": choice(["online", "idle", "dnd"]),
                    "since": 0,
                    "activities": [{
                        "name": "Whitos V3",
                        "type": 3,
                        "state": "discord.gg/mciem",
                    }],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                    "private_channels_version": "0",
                    "api_code_version": 0
                }
            }
        }))
    
    def sendMessage(self, channelID: str, guildID: str, message: str):
        headers = self.headers

        headers["authorization"]      = self.token
        headers["x-super-properties"] = self.xsup
        headers["referer"]            = f"https://discord.com/channels/{guildID}/{channelID}"

        js = {
            "content": message, 
            "tts": "false",
            "nonce": ((int(time()) * 1000) - 1420070400000) * 4194304,
        }

        req = self.session.post(f"https://discord.com/api/v9/channels/{channelID}/messages", headers=headers, proxy=self.proxy, json=js)

        if req.status_code == 200:
            self.console.debug(f"Message sent -> {message}")
    
    def getVerifyToken(self, url: str):
        headers = self.headers
        
        headers["authorization"] = self.token
        
        req = self.session.get(url, headers=headers, proxy=self.proxy, allow_redirects=True)
        
        return str(req.url).split("token=")[1] if req.status_code == 200 else None
    
    def claim(self, email: str, password: str) -> bool:
        headers = self.headers
        
        headers["authorization"]      = self.token
        headers["referer"]            = "https://discord.com/channels/@me"
        headers["x-super-properties"] = self.xsup
        
        js = {
            "email": email,
            "password": password
        }        
        
        req = self.session.patch("https://discord.com/api/v9/users/@me", json=js, headers=headers, proxy=self.proxy)
        resp = req.json()

        if req.status_code == 200:
            self.token = resp["token"]
        
        return req.status_code == 200

    def verify(self, token: str):
        headers = self.headers
        
        headers["authorization"]      = self.token
        headers["referer"]            = "https://discord.com/channels/@me"
        headers["x-super-properties"] = self.xsup
        
        js = {
            "token": token
        }
        
        req = self.session.post("https://discord.com/api/v9/auth/verify", json=js, headers=headers, proxy=self.proxy)
        resp = req.json()        
        
        if req.status_code == 200:
            self.email_verified = True
            
            self.humanized.append("email")
            
            self.token = resp["token"]
        
        return req.status_code == 200

    def addPhoneNumber(self, cap: str, number: str):
        headers = self.headers
        
        headers["authorization"]      = self.token
        headers["referer"]            = "https://discord.com/channels/@me"
        headers["x-super-properties"] = self.xsup
        
        js = {
            "phone": number,
            "captcha_key": cap,
            "change_phone_reason": "user_settings_update"
        }
        
        req = self.session.post("https://discord.com/api/v9/users/@me/phone", json=js, headers=headers, proxy=self.proxy)
        
        return req.status_code == 204

    def getPhoneToken(self, code: str, number: str):
        headers = self.headers
        
        headers["authorization"]      = self.token
        headers["referer"]            = "https://discord.com/channels/@me"
        headers["x-super-properties"] = self.xsup
        
        js = {
            "code": code,
            "phone": number,
        }
        
        req = self.session.post("https://discord.com/api/v9/phone-verifications/verify", json=js, headers=headers, proxy=self.proxy)
        
        return req.json()
    
    def sumbitSMS(self, password: str, token: str):
        headers = self.headers
        
        headers["authorization"]      = self.token
        headers["referer"]            = "https://discord.com/channels/@me"
        headers["x-super-properties"] = self.xsup
        
        js = {
            "change_phone_reason": "user_settings_update",
            "password": password,
            "phone_token": token
        }

        req = self.session.post("https://discord.com/api/v9/users/@me/phone", json=js, headers=headers, proxy=self.proxy)

        if req.status_code == 204:
            self.phone_verified = True
            
            self.humanized.append("phone")
        
        return req.status_code == 204