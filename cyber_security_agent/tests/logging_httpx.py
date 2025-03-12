import httpx
import time
import logging

logging.basicConfig(filename="monitor_httpx.log", level=logging.INFO, format="%(asctime)s - %(message)s")

url = "https://taupe-tanuki-66c44a.netlify.app/"

def check_website():
    while True:
        try:
            start = time.time()
            response = httpx.get(url, timeout=5)
            duration = time.time() - start

            if response.status_code == 200:
                logging.info(f"✅ UP: {url} - Response time: {duration:.2f}s")
            else:
                logging.warning(f"⚠️ DOWN: {url} - Status Code: {response.status_code}")
        except Exception as e:
            logging.error(f"❌ ERROR: {url} - {e}")
        time.sleep(10)

check_website()
