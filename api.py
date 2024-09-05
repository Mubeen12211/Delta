from fastapi import FastAPI, Request
import requests
import re

app = FastAPI()

# Regular expression to capture key or token from response content
key_regex = r'let content = \("([^"]+)"\);'

# Function to fetch the URL with appropriate headers and referers
def fetch_with_referer(url, referer=None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'close',
        'Referer': referer if referer else '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
    try:
        # Sending GET request to the URL with referer
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch URL: {url}. Error: {e}")

# Function to bypass the link and extract the content key
def bypass_links(url1, url2, referer1, referer2):
    try:
        # Step 1: Fetch the first link with referer
        response_text_1 = fetch_with_referer(url1, referer1)

        # Step 2: Fetch the second link with a different referer
        response_text_2 = fetch_with_referer(url2, referer2)

        # Try to extract content key from the response of the second URL
        match = re.search(key_regex, response_text_2)
        if match:
            return match.group(1)  # Return the extracted key
        else:
            raise Exception("Failed to extract key from the response.")
    
    except Exception as e:
        raise Exception(f"Failed to bypass link. Error: {e}")

@app.get("/")
def home():
    return {"message": "Invalid Endpoint"}

@app.get("/api/bypass")
def bypass(request: Request):
    # Extract the URLs and referers from the query parameters
    url1 = request.query_params.get("url1")
    referer1 = request.query_params.get("referer1")
    url2 = request.query_params.get("url2")
    referer2 = request.query_params.get("referer2")

    if not url1 or not url2 or not referer1 or not referer2:
        return {"message": "Please provide valid URLs and referers"}, 400
    
    try:
        # Call the bypass_links function with the provided URLs and referers
        content_key = bypass_links(url1, url2, referer1, referer2)
        return {"key": content_key, "status": "success"}
    except Exception as e:
        return {"error": str(e)}, 500
