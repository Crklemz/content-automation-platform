import os
import requests
from requests.auth import HTTPBasicAuth

WP_API_URL = os.getenv("WP_API_URL")
WP_API_USER = os.getenv("WP_API_USER")
WP_API_PASSWORD = os.getenv("WP_API_PASSWORD")

def publish_to_wordpress(title, content, status="pending"):
    url = f"{WP_API_URL}/posts"

    data = {
        "title": title,
        "content": content,
        "status": status,  # publish | draft | pending
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(WP_API_USER, WP_API_PASSWORD)
    )

    if response.status_code == 201:
        print("✅ Successfully published to WordPress!")
        print("Post URL:", response.json().get("link"))
    else:
        print("❌ Failed to publish.")
        print("Status:", response.status_code)
        print("Response:", response.text)
