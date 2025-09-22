import tempfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_channel_videos(channel_url, max_videos=10):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # FIX: create a unique temp user data directory
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    # Use webdriver-manager to install ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(channel_url)

    driver.implicitly_wait(5)
    videos = []

    try:
        video_elements = driver.find_elements(By.XPATH, '//a[@id="video-title"]')[:max_videos]
        for video in video_elements:
            title = video.get_attribute("title")
            url = video.get_attribute("href")
            video_id = url.split("v=")[-1] if url else None
            videos.append({
                "title": title,
                "url": url,
                "video_id": video_id
            })
    except Exception as e:
        print(f"Error extracting videos: {e}")
    finally:
        driver.quit()

    return videos
