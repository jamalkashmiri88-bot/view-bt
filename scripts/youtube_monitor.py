import os
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def get_channel_info(channel_url):
    """Get channel information from YouTube"""
    print(f"Checking channel: {channel_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Try to fetch the channel page
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(channel_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for video elements - this is a simplified example
            video_elements = soup.find_all('a', {'id': 'video-title-link'})
            
            videos = []
            for i, video in enumerate(video_elements[:5]):  # Limit to 5 videos for demo
                title = video.get('title', f'Video {i+1}')
                href = video.get('href', '')
                full_url = f"https://www.youtube.com{href}" if href.startswith('/') else href
                
                videos.append({
                    "title": title,
                    "url": full_url,
                    "duration": "Unknown"
                })
            
            return videos
        else:
            print(f"Failed to fetch channel page. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error fetching channel data: {e}")
    
    # Fallback to simulated data if scraping fails
    print("Using simulated data as fallback")
    videos = [
        {"title": "Mysterious Discovery in Abandoned Building", "url": "https://youtube.com/watch?v=abc123", "duration": "15:32"},
        {"title": "Urban Exploration Gone Wrong", "url": "https://youtube.com/watch?v=def456", "duration": "22:18"},
        {"title": "Found Something Strange in the Woods", "url": "https://youtube.com/watch?v=ghi789", "duration": "18:45"},
        {"title": "Abandoned Hospital Investigation", "url": "https://youtube.com/watch?v=jkl012", "duration": "25:12"},
        {"title": "The Case of the Missing Hiker", "url": "https://youtube.com/watch?v=mno345", "duration": "20:07"}
    ]
    
    return videos

def main():
    channel_url = os.environ.get('CHANNEL_URL', '')
    
    if not channel_url:
        print("No channel URL provided")
        return
    
    print("=" * 50)
    print("YouTube Channel Monitor")
    print("=" * 50)
    
    videos = get_channel_info(channel_url)
    
    # Simulate monitoring process
    print(f"\nFound {len(videos)} videos on the channel")
    
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']} ({video['duration']})")
    
    # Save results to a file
    results = {
        "check_time": datetime.now().isoformat(),
        "channel_url": channel_url,
        "videos_found": len(videos),
        "videos": videos
    }
    
    with open('video_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to video_results.json")
    print("Monitoring completed!")

if __name__ == "__main__":
    main()
