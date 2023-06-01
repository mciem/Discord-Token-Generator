import httpx

class Onlinesim:
    def __init__(self, key: str, number_code: int) -> None:
        self.headers = {"accept": "application/json"}

        self.key = key
        self.number_code = number_code
        self.balance = self.getBalance()
        
    
    def getBalance(self):
        url = f"https://onlinesim.ru/api/getBalance.php?apikey={self.key}"
        
        req = httpx.get(url, headers=self.headers)
        js = req.json()
        
        if js.get("response") == "1":
            return js.get("balance")
        else:
            return
    
    def getNumber(self):
        url = f"https://onlinesim.ru/api/getNum.php?apikey={self.key}&service=discord&number=true&country={self.number_code}"

        req = httpx.get(url, headers=self.headers)
        js = req.json()
        
        if js.get("response") == 1:
            return js.get("number"), js.get("tzid")
        else:
            return
    
    def getState(self, tzid: str):
        url = f"https://onlinesim.ru/api/getState.php?apikey={self.key}&tzid={tzid}"
        
        req = httpx.get(url, headers=self.headers)
        js = req.json()
        
        return js[0].get("msg")

class VakSMS:
    def __init__(self, key: str, number_code: str) -> None:
        self.headers = {"accept": "application/json"}

        self.key = key
        self.number_code = number_code
        self.balance = self.getBalance()
    
    def getBalance(self):
        url = f"https://vak-sms.com/api/getBalance/?apiKey={self.key}"
        
        req = httpx.get(url, headers=self.headers)
        js = req.json()
        
        return js.get("balance")

    def getNumber(self):
        url = f"https://vak-sms.com/api/getNumber/?apiKey={self.key}&service=discord&country={self.number_code}"
        
        req = httpx.get(url, headers=self.headers)
        js = req.json()
        
        return js.get("tel"), js.get("idNum")
    
    def getState(self, idNum: str):
        url = f"https://vak-sms.com/api/getSmsCode/?apiKey={self.key}&idNum={idNum}"
        
        req = httpx.get(url, headers=self.headers)
        js = req.json()
        
        return js.get("smsCode")
    