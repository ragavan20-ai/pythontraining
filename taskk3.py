
import requests
import os
import hmac
import hashlib

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not API_KEY or not WEBHOOK_SECRET:
    raise ValueError("API_KEY or WEBHOOK_SECRET is missing in .env")


# Create retry configuration
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)


# Create requests session
session = requests.Session()

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


# GET API request
url = "https://jsonplaceholder.typicode.com/users"

response = session.get(url, timeout=10)
response.raise_for_status()

users = response.json()


# Print first 5 users
for user in users[:5]:
    print(
        user.get("id", "Not Available"),
        "-",
        user.get("name", "Not Available"),
        "-",
        user.get("email", "Not Available")
    )


# Get first user's details using .get()
first_user = users[0]

address = first_user.get("address", {})
geo = address.get("geo", {})
company = first_user.get("company", {})

city = address.get("city", "Not Available")
latitude = geo.get("lat", "Not Available")
zip_code = address.get("zip", "Not Available")
company_name = company.get("name", "Not Available")

print("\nCity:", city, "| Zip:", zip_code)
print("Latitude:", latitude)
print("Company:", company_name)


# HMAC-SHA256 signature verification
def verify_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


# Test webhook security
payload = '{"message": "Hello Webhook"}'

# Generate valid signature
valid_signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    payload.encode(),
    hashlib.sha256
).hexdigest()

# Test valid signature
valid = verify_signature(
    payload, valid_signature, WEBHOOK_SECRET
)

# Test tampered payload
tampered = verify_signature(
    '{"message": "Hacked"}',
    valid_signature,
    WEBHOOK_SECRET
)

# Test wrong secret
wrong_secret = verify_signature(
    payload,
    valid_signature,
    "wrong_secret"
)

print(
    "\nValid:", valid,
    "| Tampered:", tampered,
    "| Wrong secret:", wrong_secret
)
