from fastapi import FastAPI, Request
import requests
import re
from urllib.parse import urlparse, parse_qs

app = FastAPI()

# Regex pattern to extract the content key from the response
key_regex = r'let content = \("([^"]+)"\);'

def fetch(url, headers):
    """Fetch the content of the URL with the specified headers."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch URL: {url}. Error: {e}")

def build_referer(base_referer, encoded_params):
    """Construct the referer URL by appending encoded parameters."""
    return f"{base_referer}{encoded_params}"

def bypass_link(initial_url):
    """Process the initial URL and navigate through redirections to extract content key."""
    try:
        # Extract HWID from the initial URL
        hwid_match = re.search(r'id=([^&]+)', initial_url)
        if not hwid_match:
            raise Exception("Invalid HWID in URL")
        hwid = hwid_match.group(1)

        # Define base referers and encoded parameters
        base_referers = [
            "https://loot-link.com/s?fJjn&r=",
            "https://gateway.platoboost.com/a/8?id=",
        ]

        encoded_params = [
            "aHR0cHM6Ly9nYXRld2F5LnBsYXRvYm9vc3QuY29tL2EvOD9pZD1hNjAwZjZjOWM2NDMyMmU2NDhkMTQ0ZGVkN2MxNzEyY2YzNjU3YTk2NzE4ZjlhOTk1YjI0MTRkZTg5MmQ0NGQxJnRrPWM1Nzk%3D",
            "",
        ]

        endpoints = [
            {
                "url": f"https://gateway.platoboost.com/a/8?id={hwid}",
                "referer": build_referer(base_referers[0], encoded_params[0])
            },
            {
                "url": f"https://gateway.platoboost.com/a/8?id={hwid}&tk=b6cc",
                "referer": build_referer(base_referers[1], f"{hwid}")
            }
        ]

        # Process each endpoint
        for endpoint in endpoints:
            url = endpoint["url"]
            referer = endpoint["referer"]
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',
                'Connection': 'close',
                'Referer': referer,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            }
            response_text = fetch(url, headers)

            # Extract the content key from the final endpoint
            if endpoint == endpoints[-1]:
                match = re.search(key_regex, response_text)
                if match:
                    return match.group(1)
                else:
                    raise Exception("Failed to find content key")
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Invalid Endpoint. Use /api/delta?url="}

@app.get("/api/delta")
def delta_bypass(request: Request):
    url = request.query_params.get("url")
    if not url:
        return {"message": "Please provide a URL"}, 400

    try:
        # Process the provided URL
        content_key = bypass_link(url)
        if content_key:
            return {"key": content_key, "message": "URL processed successfully"}
        else:
            return {"message": "Failed to process URL"}, 500
    except Exception as e:
        return {"error": str(e)}, 500
