import json
from datetime import datetime

# List of direct YouTube video URLs
video_urls = [
    "https://youtu.be/Xs7A52Hhfas?si=7EUn-D9axTjdzxRa",
    "https://youtu.be/Hp0LYYlaRzg?si=FLG7UJ3Zox7sUODt",
    "https://youtu.be/dIr50nmaWoQ?si=hlWwNkDklY2FsZj-",
    "https://youtu.be/WP5x48jp7yM?si=xmZpv_YIg93EPhfI",
    "https://youtu.be/gooqrZUhn5A?si=6k9PZeL0fTK6bwVn",
    "https://youtu.be/E1_7WLbg1wk?si=LiSRVBkz37uRcZZ2",
    "https://youtu.be/mCdYwZ6Wd84?si=keWbmQtQ-nk_1AHE"
]

def main():
    print("="*50)
    print(f"Monitoring {len(video_urls)} YouTube videos")
    print(f"Time: {datetime.now()}")
    print("="*50)

    if video_urls:
        print(f"Found {len(video_urls)} videos.")
        # Save to JSON
        with open("video_results.json", "w") as f:
            json.dump(video_urls, f, indent=4)
        print("Saved video URLs to video_results.json")
    else:
        print("No videos found.")

if __name__ == "__main__":
    main()
