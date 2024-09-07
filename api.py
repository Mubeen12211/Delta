import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure WebDriver (Use the path to your ChromeDriver)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_service = Service("/path/to/chromedriver")  # Path to ChromeDriver

# Initialize WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def get_key(url):
    try:
        driver.get(url)

        # Wait for the page to load and the first "Continue" button to appear
        time.sleep(5)  # Wait for the page and elements to load
        continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
        continue_button.click()

        # Wait for redirection and for the new page (e.g., 2nd image) to load
        time.sleep(5)

        # Simulate interaction on the second page (read articles, ads, etc.)
        unlock_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Unlock Content')]")
        unlock_button.click()

        # Wait for the whitelist key to appear (as in the 3rd image)
        time.sleep(5)
        key_element = driver.find_element(By.XPATH, "//div[contains(text(), 'KEY_')]")
        key = key_element.text

        # Return the extracted key
        return key

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Test URLs (You can loop through these or just use one)
urls = [
    'https://gateway.platoboost.com/a/8?id=939a149ae12216c57f15e03652adf5045d5fc5eea4b51171895496af556e11f8',
    'https://loot-link.com/s?fJjn&r=aHR0cHM6Ly9nYXRld2F5LnBsYXRvYm9vc3QuY29tL2EvOD9pZD05MzlhMTQ5YWUxMjIxNmM1N2YxNWUwMzY1MmFkZjUwNDVkNWZjNWVlYTRiNTExNzE4OTU0OTZhZjU1NmUxMWY4JnRrPWg3YWQ%3D',
    'https://gateway.platoboost.com/a/8?id=939a149ae12216c57f15e03652adf5045d5fc5eea4b51171895496af556e11f8&tk=h7ad'
]

# Fetch keys for all URLs
for url in urls:
    key = get_key(url)
    if key:
        print(f"Key for {url}: {key}")
    else:
        print(f"Failed to get key for {url}")

# Close the driver when done
driver.quit()
