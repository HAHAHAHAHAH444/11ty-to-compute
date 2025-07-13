import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

TG_TOKEN = '7103320273:AAFpP2XmVaWNzJoLckwNcNvL6IXaWqYj3cY'
TG_CHAT_ID = '7578349361'

URLS = [
    "https://www.facebook.com/marketplace/kualalumpur/search?daysSinceListed=1&sortBy=creation_time_descend&query=ip&exact=false",
    "https://www.facebook.com/marketplace/kualalumpur/search?daysSinceListed=1&sortBy=creation_time_descend&query=iphone&exact=false",
    "https://www.facebook.com/marketplace/kualalumpur/search?daysSinceListed=1&sortBy=creation_time_descend&query=urgent&exact=false"
]

sent_links = set()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {'chat_id': TG_CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_listings():
    driver = setup_driver()
    new_posts = []
    for url in URLS:
        try:
            driver.get(url)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            links = soup.find_all('a', href=True)
            for tag in links:
                href = tag['href']
                if '/marketplace/item/' in href:
                    full_link = 'https://www.facebook.com' + href.split('?')[0]
                    if full_link not in sent_links:
                        sent_links.add(full_link)
                        new_posts.append(full_link)
        except Exception as e:
            print(f"Error fetching from {url}:", e)
    driver.quit()
    return new_posts

while True:
    try:
        listings = fetch_listings()
        for link in listings:
            send_telegram(f"📢 New Listing: {link}")
    except Exception as e:
        print("Error:", e)
    time.sleep(60)
