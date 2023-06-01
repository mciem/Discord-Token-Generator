from tls_client import Session

class Client:
    def __init__(self, proxy: str, chrome_version: str) -> None:
        self.headers = {
			"accept":             "*/*",
			"accept-language":    "en-US;q=0.8,en;q=0.7",
			"content-type":       "application/json",
			"host":               "discord.com",
			"origin":             "https://discord.com",
			"sec-ch-ua":          f'"Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}", "Not;A=Brand";v="99"',
			"sec-ch-ua-mobile":   "?0",
			"sec-ch-ua-platform": '"Windows"',
			"sec-fetch-dest":     "empty",
			"sec-fetch-mode":     "cors",
			"sec-fetch-site":     "same-origin",
			"user-agent":         f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",
        }
        
        self.session = Session(client_identifier=f"chrome_{chrome_version}", random_tls_extension_order=True)
        self.proxy = "http://" + proxy
	
        self.session.get("https://discord.com", headers=self.headers, proxy=self.proxy)

        self.headers["cookie"]             = "; ".join(f"{k}={v}" for k,v in self.session.cookies.items())
        
        self.headers["x-discord-locale"]   = "pl"
        self.headers["x-discord-timezone"] = "Europe/Warsaw"
        self.headers["x-debug-options"]    = "bugReporterEnabled"