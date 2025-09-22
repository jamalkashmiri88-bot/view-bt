import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os

# -------------------------------
# CONFIG
# -------------------------------

# Paste your video URLs here
VIDEO_URLS = [
    "https://youtu.be/Xs7A52Hhfas?si=7EUn-D9axTjdzxRa",
    "https://youtu.be/Hp0LYYlaRzg?si=FLG7UJ3Zox7sUODt",
    "https://youtu.be/dIr50nmaWoQ?si=hlWwNkDklY2FsZj-",
    "https://youtu.be/WP5x48jp7yM?si=xmZpv_YIg93EPhfI",
    "https://youtu.be/gooqrZUhn5A?si=6k9PZeL0fTK6bwVn",
    "https://youtu.be/E1_7WLbg1wk?si=LiSRVBkz37uRcZZ2",
    "https://youtu.be/mCdYwZ6Wd84?si=keWbmQtQ-nk_1AHE"
]

# Number of times to visit each video
VISITS_PER_VIDEO = 100

# Output file
OUTPUT_FILE = "video_results.json"

# Path to chromedriver (default in GitHub Actions)
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# -------------------------------
# FUNCTIONS
# -------------------------------

def visit_videos(video_urls, visits_per_video=1):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    # Use unique temporary user-data-dir to avoid SessionNotCreatedException
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    results = []

    for url in video_urls:
        for visit in range(1, visits_per_video + 1):
            print(f"Visiting {url} — visit {visit}/{visits_per_video}")
            try:
                driver.get(url)
                time.sleep(1)  # wait for page to load
                results.append({"url": url, "visit": visit, "status": "visited"})
            except Exception as e:
                results.append({"url": url, "visit": visit, "status": f"error: {str(e)}"})
                print(f"❌ Error on visit {visit}: {e}")

    driver.quit()
    return results

def save_results(results, output_file=OUTPUT_FILE):
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n✅ Results saved to {output_file}")

# -------------------------------
# MAIN
# -------------------------------

def main():
    print("="*50)
    print(f"Monitoring YouTube Videos at {datetime.now()}")
    print("="*50)

    results = visit_videos(VIDEO_URLS, VISITS_PER_VIDEO)
    save_results(results)

if __name__ == "__main__":
    main()
