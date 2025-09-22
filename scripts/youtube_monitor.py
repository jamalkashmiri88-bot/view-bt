import json
import time
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_channel_videos(channel_url):
    # Chrome options
    options = Options()
    options.add_argument("--headless=new")  # headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Use unique temp user-data-dir to avoid conflicts
    temp_profile_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile_dir}")
    
    # Start Chrome driver
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # Open channel videos page
    driver.get(channel_url)
    time.sleep(5)  # wait for videos to load
    
    # Find video elements
    video_elements = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
    
    videos = []
    for v in video_elements:
        title = v.get_attribute('title')
        link = v.get_attribute('href')
        videos.append({"title": title, "url": link})
    
    driver.quit()
    return videos

def main():
    channel_url = "https://www.youtube.com/@LostAndClassified/videos"
    
    print("="*50)
    print(f"Monitoring YouTube Channel: {channel_url}")
    print(f"Time: {datetime.now()}")
    print("="*50)
    
    try:
        videos = get_channel_videos(channel_url)
        print(f"Found {len(videos)} videos on the channel.")
        
        # Save JSON
        with open("video_results.json", "w") as f:
            json.dump(videos, f, indent=4)
        
        if len(videos) == 0:
            print("No videos found.")
        else:
            for i, vid in enumerate(videos, start=1):
                print(f"{i}. {vid['title']} - {vid['url']}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
