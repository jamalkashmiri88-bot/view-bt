import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- CONFIG ---

VIDEO_URLS = [
    "https://youtu.be/Xs7A52Hhfas?si=7EUn-D9axTjdzxRa",
    "https://youtu.be/Hp0LYYlaRzg?si=FLG7UJ3Zox7sUODt",
    "https://youtu.be/dIr50nmaWoQ?si=hlWwNkDklY2FsZj-",
    "https://youtu.be/WP5x48jp7yM?si=xmZpv_YIg93EPhfI",
    "https://youtu.be/gooqrZUhn5A?si=6k9PZeL0fTK6bwVn",
    "https://youtu.be/E1_7WLbg1wk?si=LiSRVBkz37uRcZZ2",
    "https://youtu.be/mCdYwZ6Wd84?si=keWbmQtQ-nk_1AHE"
]

VISITS_PER_VIDEO = 100  # number of visits per video

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"  # default path on GitHub Actions runners

# ------------------

def visit_videos(video_urls, visits_per_video=1):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    # Remove --user-data-dir to avoid GitHub Actions session errors
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    results = []

    for url in video_urls:
        for visit in range(1, visits_per_video + 1):
            print(f"Visiting {url} — visit {visit}/{visits_per_video}")
            try:
                driver.get(url)
                time.sleep(1)  # wait 1 sec to simulate view
                results.append({"url": url, "visit": visit, "status": "visited"})
            except Exception as e:
                results.append({"url": url, "visit": visit, "status": f"error: {str(e)}"})
                print(f"❌ Error on visit {visit}: {e}")

    driver.quit()
    return results

def main():
    print("="*50)
    print("Monitoring YouTube Videos")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    results = visit_videos(VIDEO_URLS, VISITS_PER_VIDEO)

    # Save results to JSON
    with open("video_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Finished! Results saved to video_results.json")
    print(f"Total visits: {len(results)}")

if __name__ == "__main__":
    main()
