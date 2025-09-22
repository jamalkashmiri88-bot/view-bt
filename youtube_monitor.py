import os
import json
from datetime import datetime
from googleapiclient.discovery import build

def get_channel_videos(api_key, channel_id):
    """Fetch video information from a YouTube channel using the API"""
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # First, get the uploads playlist ID of the channel
    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    
    if not channel_response['items']:
        print(f"Channel with ID {channel_id} not found.")
        return []
    
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Now get the videos from the uploads playlist
    videos = []
    next_page_token = None
    
    try:
        while True:
            playlist_response = youtube.playlistItems().list(
                playlistId=uploads_playlist_id,
                part='snippet',
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append({
                    'title': video_title,
                    'url': video_url
                })
            
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
                
    except Exception as e:
        print(f"Error fetching videos: {e}")
    
    return videos

def main():
    api_key = os.environ.get('YOUTUBE_API_KEY')
    channel_id = os.environ.get('CHANNEL_ID')
    
    if not api_key:
        print("YouTube API key not found.")
        return
    
    if not channel_id:
        print("Channel ID not provided.")
        return
    
    videos = get_channel_videos(api_key, channel_id)
    
    # Save results to a file
    results = {
        "check_time": datetime.now().isoformat(),
        "channel_id": channel_id,
        "videos_found": len(videos),
        "videos": videos
    }
    
    with open('video_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Found {len(videos)} videos for channel {channel_id}")

if __name__ == "__main__":
    main()
