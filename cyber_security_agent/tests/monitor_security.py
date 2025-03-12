from loguru import logger
import requests

BASE_URL = "https://taupe-tanuki-66c44a.netlify.app"

logger.add("security_logs.log", rotation="10 MB")

def monitor_logs():
    try:
        response = requests.get(BASE_URL)
        logger.info(f"Status: {response.status_code}, Headers: {response.headers}")
    except Exception as e:
        logger.error(f"Monitoring failed: {e}")

monitor_logs()
