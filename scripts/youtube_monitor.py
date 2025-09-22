import os
import json
import tempfile
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def get_channel_videos(channel_url, max_videos=10):
    print("="*50)
    print(f"Monitoring YouTube Channel: {channel_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Use a temporary, unique user data directory to prevent session errors
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    # Install ChromeDriver automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    videos = []
    try:
        driver.get(channel_url)
        driver.implicitly_wait(5)

        # Find videos using the video title links
        video_elements = driver.find_elements(By.XPATH, '//a[@id="video-title"]')[:max_videos]
        for i, video in enumerate(video_elements, start=1):
            title = video.get_attribute("title")
            url = video.get_attribute("href")
            video_id = url.split("v=")[-1] if url else None
            videos.append({
                "title": title,
                "url": url,
                "video_id": video_id
            })
            print(f"{i}. {title}")
            print(f"   URL: {url}")
            if video_id:
                print(f"   ID: {video_id}")
            print()

        print(f"Total videos found: {len(videos)}")

    except Exception as e:
        print(f"Error extracting videos: {e}")
    finally:
        driver.quit()

    return videos

def main():
    channel_url = os.environ.get("CHANNEL_URL")
    if not channel_url:
        print("No CHANNEL_URL provided")
        return

    videos = get_channel_videos(channel_url)

    # Save results to JSON
    results = {
        "check_time": datetime.now().isoformat(),
        "channel_url": channel_url,
        "videos_found": len(videos),
        "videos": videos
    }

    with open("video_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Results saved to video_results.json")

if __name__ == "__main__":
    main()
