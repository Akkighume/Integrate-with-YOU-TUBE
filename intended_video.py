from googleapiclient.discovery import build
from prettytable import PrettyTable
import duckdb

# YouTube API key and channel username
yt_key_api = 'AIzaSyA6ncSvli_dcNasQPD4t4xzpjhn0vgpG4U'
channel_username = 'NitishRajput'

video_id = 'AcdLji_Umn4'  # Replace with the actual video ID

# Build YouTube API service
youtube = build('youtube', 'v3', developerKey=yt_key_api)

# Function to get channel stats by username
def get_channel_stats_by_username():
    request = youtube.channels().list(part='snippet,statistics', forUsername=channel_username)
    response = request.execute()

    if 'items' not in response or not response['items']:
        return None

    return {
        'channel_name': response['items'][0]['snippet']['title'],
        'subscribers': response['items'][0]['statistics']['subscriberCount'],
        'views': response['items'][0]['statistics']['viewCount'],
        'total_videos': response['items'][0]['statistics']['videoCount']
    }

# Function to get video metrics
def get_video_metrics():
    request = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id)
    response = request.execute()

    if 'items' not in response or not response['items']:
        return None

    video_data = response['items'][0]['statistics']
    snippet_data = response['items'][0]['snippet']
    return {
        'total_views_per_video': video_data.get('viewCount', 0),
        'number_of_likes': video_data.get('likeCount', 0),
        'number_of_dislikes': video_data.get('dislikeCount', 0),
        'video_engagement': video_data.get('commentCount', 0),
        'video_comments': snippet_data.get('commentCount', 0)
    }

# Connect to DuckDB database
conn = duckdb.connect('youtube_data.db')

# Create tables if not exists
conn.execute('CREATE TABLE IF NOT EXISTS channel_stats (channel_name VARCHAR, subscribers BIGINT, views BIGINT, total_videos BIGINT)')
# Modify the table schema to include the video_comments column
conn.execute('CREATE TABLE IF NOT EXISTS video_metrics (total_views_per_video BIGINT, number_of_likes BIGINT, number_of_dislikes BIGINT, video_engagement BIGINT, video_comments BIGINT)')


# Print PrettyTable
def print_pretty_table(data, title):
    if data is None:
        print(f"No data available for {title}")
        return

    table = PrettyTable()
    table.field_names = [title, 'Value']

    for key, value in data.items():
        table.add_row([key, value])

    print(table)

# Get and print results
channel_stats = get_channel_stats_by_username()
video_metrics = get_video_metrics()

print_pretty_table(channel_stats, "Channel Statistics")
print_pretty_table(video_metrics, "Video Metrics")

# Insert data into DuckDB tables
if channel_stats:
    conn.execute('INSERT INTO channel_stats VALUES (?, ?, ?, ?)', (channel_stats['channel_name'], channel_stats['subscribers'], channel_stats['views'], channel_stats['total_videos']))
    print("Channel statistics inserted successfully.")

if video_metrics:
    conn.execute('INSERT INTO video_metrics VALUES (?, ?, ?, ?)', (video_metrics['total_views_per_video'], video_metrics['number_of_likes'], video_metrics['number_of_dislikes'], video_metrics['video_engagement']))
    print("Video metrics inserted successfully.")




# Close DuckDB connection
conn.close()
