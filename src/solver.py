from httpx import Client
from time  import sleep

class Solver:
    def __init__(self, api: str, key: str) -> None:
        if api == "capsolver.com":
            self.typ = "HCaptchaTurboTask"
        else:
            self.typ = "HCaptchaTask"
            
        self.api = api
        self.key = key
        
        self.headers = {
            "Host": f"api.{api}",
            "Content-Type": "application/json"      
        }
        
        self.session = Client()
        
        self.balance = self.getBalance()
        
        if not self.balance:
            Exception("Invalid key")
    
    def getBalance(self) -> float:
        payload = {
            "clientKey": self.key
        }
        
        req = self.session.post(f"https://api.{self.api}/getBalance", headers=self.headers, timeout=15, json=payload)
        js = req.json()
        
        if js["errorId"] == 0:
            return js["balance"]
        else:
            return 
    
    def reformatProxy(self, proxy: str) -> str:
        user, password, host, port = proxy.split(":")[0], proxy.split("@")[0].split(":")[1], proxy.split("@")[1].split(":")[0], proxy.split("@")[1].split(":")[1]

        return f"http:{host}:{port}:{user}:{password}"

    def solveCaptcha(self, proxy: str, sitekey: str = "4c672d35-0701-42b2-88c3-78380b0db560") -> str:
        proxy = self.reformatProxy(proxy)
        
        payload = {
            "clientKey": self.key,
            "task": {
                "type": self.typ,
                "websiteURL": "https://discord.com/",
                "websiteKey": sitekey,
                "proxy": proxy,
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }
        }
        
        req = self.session.post(f"https://api.{self.api}/createTask", json=payload, headers=self.headers, timeout=15)
        js = req.json()
        
        if js["errorId"] == 0:
            taskId = js["taskId"]
        else:
            return js["errorDescription"]

        req = self.session.post(f"https://api.{self.api}/getTaskResult", json={"taskId": taskId}, headers=self.headers, timeout=15)
        js = req.json()
        
        while js["status"] != "ready":
            req = self.session.post(f"https://api.{self.api}/getTaskResult", json={"taskId": taskId}, headers=self.headers, timeout=15)
            js = req.json()
                        
            sleep(1)
        
        return js["solution"]["gRecaptchaResponse"]
        