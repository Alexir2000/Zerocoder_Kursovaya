import os
import ssl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Путь к вашим сертификатам
CERTIFICATE_FILE = os.path.join(BASE_DIR, 'localhost.pem')
KEY_FILE = os.path.join(BASE_DIR, 'localhost-key.pem')

print(f"BASE_DIR: {BASE_DIR}")
print(f"CERTIFICATE_FILE: {CERTIFICATE_FILE}")
print(f"KEY_FILE: {KEY_FILE}")