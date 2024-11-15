import os
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.porncucumber.com/videos/"

# Function to fetch video data for a specific folder
def fetch_video_data(video_folder):
    folder_url = f"{BASE_URL}{video_folder}/"
    response = requests.get(folder_url)
    if response.status_code != 200:
        print(f"Failed to fetch data for folder: {video_folder}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    video_data = {}

    # Extract video name, URL, and generate thumbnails
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.mp4'):
            video_url = f"{folder_url}{href}"
            video_name = os.path.splitext(href)[0].replace('%20', ' ')
            video_id = video_folder  # Using folder name as unique ID
            thumbnails = [
                f"{folder_url}{href.replace('.mp4', f'_thumbnail{i}.jpg')}" for i in range(1, 5)
            ]

            # Construct video data
            video_data[video_id] = {
                "name": video_name,
                "video_url": video_url,
                "thumbnails": thumbnails
            }

    return video_data

# Function to fetch all available video folders
def get_video_folders():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed to fetch video folders from base URL.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    folders = []

    # Extract folder links
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('/'):  # Assuming folders have trailing slashes
            folder_name = href.strip('/')
            folders.append(folder_name)

    return folders[:200]  # Limit to 200 folders

# Main function to fetch and save video data
def main():
    video_folders = get_video_folders()
    all_video_data = {}

    if not video_folders:
        print("No video folders found.")
        return

    for folder in video_folders:
        print(f"Fetching data for folder: {folder}")
        data = fetch_video_data(folder)
        if data:
            all_video_data.update(data)

    # Save all video data to JSON
    with open('video_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_video_data, f, indent=4, ensure_ascii=False)

    print("Video data successfully fetched and saved to video_data.json.")

if __name__ == "__main__":
    main()
