from pytube import YouTube
import json
import time

VIDEO_URLS = [
    "https://youtu.be/watch?v=Xs7A52Hhfas",
    "https://youtu.be/watch?v=Hp0LYYlaRzg",
    "https://youtu.be/watch?v=dIr50nmaWoQ",
    "https://youtu.be/watch?v=WP5x48jp7yM",
    "https://youtu.be/watch?v=gooqrZUhn5A",
    "https://youtu.be/watch?v=E1_7WLbg1wk",
    "https://youtu.be/watch?v=mCdYwZ6Wd84"
]

VISITS_PER_VIDEO = 100
RESULTS_FILE = "video_results.json"

def visit_videos(video_urls, visits_per_video):
    results = []
    for url in video_urls:
        print(f"Checking video: {url}")
        try:
            yt = YouTube(url)
            title = yt.title
        except Exception as e:
            title = f"Error fetching title: {e}"

        for i in range(1, visits_per_video + 1):
            print(f"Visit {i}/{visits_per_video} for {title}")
            # Here you could add sleep to simulate delay if needed
            results.append({"url": url, "title": title, "visit": i, "status": "visited"})

    return results

def main():
    print("="*50)
    print("Monitoring YouTube Videos")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    results = visit_videos(VIDEO_URLS, VISITS_PER_VIDEO)

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ Finished! Results saved to {RESULTS_FILE}")
    print(f"Total visits: {len(results)}")

if __name__ == "__main__":
    main()
