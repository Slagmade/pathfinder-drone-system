import requests
from Crypto.Cipher import AES
import base64

def send_to_rescue_team(data):
    key = b'Sixteen byte key'  # For demo only
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(str(data).encode())
    
    response = requests.post(
        "https://webhook.site/your-unique-url",  # Replace with your URL
        json={
            'nonce': base64.b64encode(cipher.nonce).decode(),
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'tag': base64.b64encode(tag).decode()
        }
    )
    return response.status_code == 200
