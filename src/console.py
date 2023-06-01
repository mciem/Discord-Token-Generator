from datetime import datetime
from colorama import Fore
from threading import RLock

class Console:
    def __init__(self) -> None:
        self.lock = RLock()
    
    def error(self, txt: str) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.lock:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTRED_EX}ERROR {Fore.LIGHTWHITE_EX}{txt}", flush=True)
    
    def debug(self, txt: str) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.lock:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTBLUE_EX}DEBUG {Fore.LIGHTWHITE_EX}{txt}", flush=True)

    def solved(self, txt: str, e: float) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.lock:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] \033[35mSOLVED {Fore.LIGHTWHITE_EX}{txt}{Fore.LIGHTBLACK_EX} | {Fore.LIGHTWHITE_EX}{str(e)}s", flush=True)

    def unlocked(self, txt: str, flags: str) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.lock:
            if flags == "SPAMMER":
                print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}UNLOCKED {Fore.LIGHTWHITE_EX}{txt[:32]}****{Fore.LIGHTBLACK_EX} | {Fore.LIGHTWHITE_EX}{flags}", flush=True)
            else:
                print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}UNLOCKED {Fore.LIGHTWHITE_EX}{txt[:32]}****{Fore.LIGHTBLACK_EX}", flush=True)
    
    def locked(self, txt: str, flags: str) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.lock:
            if flags == "SPAMMER":
                print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTYELLOW_EX}LOCKED {Fore.LIGHTWHITE_EX}{txt[:32]}****{Fore.LIGHTBLACK_EX} | {Fore.LIGHTWHITE_EX}{flags}", flush=True)
            else:
                print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTYELLOW_EX}LOCKED {Fore.LIGHTWHITE_EX}{txt[:32]}****{Fore.LIGHTBLACK_EX}", flush=True)

    def websocket(self, txt: str) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        with self.lock:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTCYAN_EX}WEBSOCKET {Fore.LIGHTWHITE_EX}{txt}", flush=True)
    
    def success(self, txt: str) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.lock:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTGREEN_EX}SUCCESS {Fore.LIGHTWHITE_EX}{txt}", flush=True)
    
    def humanized(self, token: str, L: list) -> None:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        data = "("
        x    = 0
        for l in L:
            if x == len(L) - 1:
                data += f"{l}"
            else:
                data += f"{l} "
            
        data += ")"
        
        with self.lock:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTMAGENTA_EX}HUMANIZED {Fore.LIGHTWHITE_EX}{data} -> {token[:32]}****", flush=True)
    
    def input(self, txt: str) -> str:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTBLACK_EX}{current_time}{Fore.LIGHTWHITE_EX}] {Fore.LIGHTCYAN_EX}INPUT {Fore.LIGHTWHITE_EX}{txt}", end="", flush=True)
        return input("")