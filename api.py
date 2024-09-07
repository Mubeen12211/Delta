from flask import Flask, jsonify, request
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

# Install chromedriver automatically
chromedriver_autoinstaller.install()

urls = [
    "https://gateway.platoboost.com/a/8?id=",
    "https://loot-link.com/s?fJjn&r=aHR0cHM6Ly9nYXRld2F5LnBsYXRvYm9vc3QuY29tL2EvOD9pZD05MzlhMTQ5YWUxMjIxNmM1N2YxNWUwMzY1MmFkZjUwNDVkNWZjNWVlYTRiNTExNzE4OTU0OTZhZjU1NmUxMWY4JnRrPWg3YWQ=",
]

keys = {
    "939a149ae12216c57f15e03652adf5045d5fc5eea4b51171895496af556e11f6": 0,  # first URL
    "another_dynamic_key_for_second_url": 1,  # second URL placeholder
}

@app.route('/get_key', methods=['GET'])
def get_key():
    key = request.args.get('key')

    if not key:
        return jsonify({'error': 'Key is required'}), 400

    if key not in keys:
        return jsonify({'error': 'Invalid key provided'}), 404

    # Find which base URL to use
    url_idx = keys[key]
    full_url = urls[url_idx] + key

    # Selenium ChromeDriver setup
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.binary_location = "/usr/bin/google-chrome"

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(full_url)

        # Simulate waiting for the key generation process
        driver.implicitly_wait(5)

        # Example of key extraction, adjust the XPath accordingly
        key_element = driver.find_element_by_xpath("//span[contains(@class, 'whitelist-key')]")
        generated_key = key_element.text

        driver.quit()

        return jsonify({'success': True, 'generated_key': generated_key})

    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
