from src       import *
from time      import time, sleep
from threading import Thread

import ctypes

class WhitosV3:
    def __init__(self) -> None:
        self.chrome_version = "113"
        
        self.utils = Utils()
        self.console = Console()
        
        self.xsup = self.utils.XSuperProperties(self.utils.getBuildNum(), self.chrome_version)
        
        self.unlocked, self.locked, self.ev, self.fv, self.pv = 0, 0, 0, 0, 0
    
    def title(self):
        start = time()
        while True:
            try:
                if self.locked != 0 or self.unlocked != 0:
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Whitos V3 | FV: {self.fv} | PV: {self.pv} | EV: {self.ev} | Unlocked: {self.unlocked} | Locked: {self.locked} | Unlock Rate: {round((self.unlocked/(self.locked+self.unlocked))*100, 2)}% | Time: {round(time() - start, 2)}s")
                else:
                    ctypes.windll.kernel32.SetConsoleTitleW(f"Whitos V3 | FV: {self.fv} | PV: {self.pv} | Unlocked: {self.unlocked} | Locked: {self.locked} | Unlock Rate: None | Time: {round(time() - start, 2)}s")
            except:
                continue
            
            sleep(0.01)
            
    def whitos(self, invite: str):
        while True:
            try:
                proxy = self.utils.randomProxy()
                name  = self.utils.randomName()
                
                dc = Discord(proxy, self.xsup, self.utils, self.console, self.chrome_version)
                
                start = time()
                hcap = self.solver.solveCaptcha(proxy)
                if len(hcap) < 50:
                    self.console.error(hcap)
                    continue
                
                end = time()
                
                self.console.solved(hcap[:32], round(end - start,3))
                
                dc.generate(hcap, name, invite)
                
                match dc.unlocked:
                    case True:               
                        claimed = False
                                 
                        self.unlocked += 1
                        
                        self.console.unlocked(dc.token, dc.flags)
                        
                        if dc.flags == "SPAMMER":
                            continue
                        
                        dc.setBirthdate()
                        dc.setBio(self.utils.randomBio())
                        dc.setAvatar(self.utils.randomAvatar())
                        
                        if self.utils.email_verify:
                            if self.utils.imap:
                                mail, mail_password = self.utils.randomEmail()
                                imap = IMAP(self.mail, mail_password, self.utils.imap_ssl_url)
                            else:
                                mailJSON = self.kopeechka.getMail()
                                
                                if mailJSON != None:
                                    mail = mailJSON["mail"]
                                    idd = mailJSON["id"]
                                else:
                                    with open("data/tokens.txt", "a") as f:
                                        f.write(dc.token + "\n")

                                    continue
                            password = self.utils.randomPassword()
                            
                            st = dc.claim(mail, password)
                            if st:
                                claimed = True
                                
                                self.console.debug(f"Account claimed -> {mail}:{password}")
                                
                                if self.utils.imap:
                                    x    = 0
                                    link = imap.getLink()
                                    
                                    while link == None:
                                        x += 1
                                        if x == 30:
                                            break
                                        
                                        link = imap.getLink()

                                        sleep(1)
                                else:
                                    link = self.kopeechka.checkMailbox(idd)
                                    
                                    while link == None:
                                        link = self.kopeechka.checkMailbox(idd)
                                        
                                        sleep(1)
                                    
                                    self.kopeechka.deleteMail(idd)
                                
                                if link:
                                    token = dc.getVerifyToken(link)
                                    self.console.debug(f"Verify token -> {token}")
                                    
                                    st = dc.verify(token)
                                    if st:
                                        self.console.success(f"Email verified -> {dc.token[:32]}****")         
                                    else:
                                        self.console.error("Failed to verify email")
                                else:                           
                                    self.console.error("Failed to get verify link")
                            else:                        
                                self.console.error("Failed to claim account")
                        
                        if self.utils.phone_verify:
                            if not claimed:
                                password = self.utils.randomPassword()
                                email = f"{password}@gmail.com"
                                
                                if dc.claim(email, password):
                                    self.console.debug(f"Account claimed -> {email}:{password}")
                                else:
                                    self.console.error("Failed to claim account")
                                    continue
                                
                            s = self.phone.getNumber()
                            
                            if s == None:                 
                                self.console.error("Failed to get phone number")
                                continue
                            
                            phone, tzid = s
                            
                            start = time()
                            hcap = self.solver.solveCaptcha(proxy, "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34")
                            if len(hcap) < 50:
                                self.console.error(hcap)
                                continue
                            
                            end = time()
                            
                            self.console.solved(hcap[:32], round(end - start,3))
                            
                            if dc.addPhoneNumber(hcap, phone):
                                self.console.debug(f"Phone number added -> {phone}")
                            else:                
                                self.console.error("Failed to add phone number")
                                continue
                            
                            code = None
                            while code == None:
                                sleep(3)
                                
                                code = self.phone.getState(tzid)
                                if code == None:
                                    continue
                                
                                self.console.debug(f"SMS code -> {code}")
                                     
                            token = dc.getPhoneToken(code, phone).get("token")
                            
                            if token != None:                                
                                if dc.sumbitSMS(password, token):
                                    self.console.success(f"Phone verified -> {dc.token[:32]}****")                             
                                else:
                                    self.console.error("Failed to verify phone")
                            else:
                                self.console.error("Failed to get phone token")
                        
                        if dc.email_verified and dc.phone_verified:
                            self.fv += 1
                            
                            with open("data/tokens/fv_tokens.txt", "a") as f:
                                f.write(f"{mail}:{password}:{dc.token}" + "\n")
                                
                        elif dc.email_verified:
                            self.ev += 1
                            
                            with open("data/tokens/ev_tokens.txt", "a") as f:
                                f.write(f"{mail}:{password}:{dc.token}" + "\n")
                        elif dc.phone_verified:
                            self.pv += 1
                            
                            with open("data/tokens/pv_tokens.txt", "a") as f:
                                f.write(f"{mail}:{password}:{dc.token}" + "\n")
                        
                        else:
                            with open("data/tokens/tokens.txt", "a") as f:
                                f.write(dc.token + "\n")
                        
                        if dc.humanized != []:
                            self.console.humanized(dc.token, dc.humanized)
                            
                    case False:
                        self.locked += 1
                        
                        self.console.locked(dc.token, dc.flags)
                    
                    case None:
                        self.console.error(dc.token)

            except Exception as e:
                self.console.error(str(e))
        
    def start(self):
        if self.utils.email_verify and not self.utils.imap:
            self.kopeechka = Kopeechka(self.utils.kopeechka_key)
            if self.kopeechka.balance == None:
                self.console.error("Invalid kopeechka key")
                exit()
            self.console.debug(f"Kopeechka balance: {self.kopeechka.balance}RUB")
        
        if self.utils.phone_verify:
            
            if self.utils.api_type == "vaksms":
                self.phone = VakSMS(self.utils.vaksms_key, 48)
                if self.phone.balance == None:
                    self.console.error("Invalid vaksms key")
                    exit()
                self.console.debug(f"vaksms balance: {self.phone.balance}$")
            elif self.utils.api_type == "onlinesim":    
                self.phone = Onlinesim(self.utils.onlinesim_key, 48)
                if self.phone.balance == None:
                    self.console.error("Invalid onlinesim key")
                    exit()
                self.console.debug(f"onlinesim balance: {self.onlinesim.balance}$")
            else:
                self.console.error("Invalid sms api (use onlinesim/vaksms)")
                exit()

                
        
        self.solver = Solver(self.utils.api, self.utils.key)
        if self.solver.balance == None:
            self.console.error("Invalid capsolver key")
            exit()
        self.console.debug(f"capsolver balance: {self.solver.balance}$")

        
        threads = self.console.input("Threads > ")
        invite = self.console.input("Invite > ")
        
        Thread(target=self.title).start()
        
        for _ in range(int(threads)):
            Thread(target=self.whitos, args=(invite,)).start()
        

WhitosV3().start()