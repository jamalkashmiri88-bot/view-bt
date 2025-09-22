import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

def get_channel_videos(channel_url, max_videos=10):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(channel_url)

    # Wait for page to load
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

def main():
    channel_url = os.environ.get("CHANNEL_URL", "")
    if not channel_url:
        print("No CHANNEL_URL provided")
        return

    print("="*50)
    print(f"Monitoring YouTube Channel: {channel_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    videos = get_channel_videos(channel_url)
    print(f"Found {len(videos)} videos:\n")
    for i, v in enumerate(videos, 1):
        print(f"{i}. {v['title']}")
        print(f"   URL: {v['url']}")
        print(f"   ID: {v['video_id']}\n")

    # Save to JSON
    results = {
        "check_time": datetime.now().isoformat(),
        "channel_url": channel_url,
        "videos_found": len(videos),
        "videos": videos
    }

    with open("video_results.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Results saved to video_results.json")

if __name__ == "__main__":
    main()
