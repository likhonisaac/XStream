import os
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.porncucumber.com/videos/"

# Function to fetch and parse the page to get video data
def fetch_video_data(video_folder):
    folder_url = f"{BASE_URL}{video_folder}/"
    response = requests.get(folder_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Collect video info
    video_data = {}
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.mp4'):
            video_url = f"{folder_url}{href}"
            thumbnail_url = f"{folder_url}{href.replace('.mp4', '.jpg')}"
            video_data[video_folder] = {
                'video_url': video_url,
                'thumbnail_url': thumbnail_url
            }

    return video_data

# Function to get all available video folders from the base URL
def get_video_folders():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links to video folders (directories)
    folders = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('/'):  # Assuming folders have a trailing slash
            folder_name = href.strip('/')
            folders.append(folder_name)

    return folders

# Main function to collect video data and save to JSON
def main():
    video_folders = get_video_folders()  # Automatically fetch the list of video folders
    all_video_data = {}

    for folder in video_folders:
        print(f"Fetching data for folder: {folder}")
        data = fetch_video_data(folder)
        all_video_data.update(data)

    # Save the video data to a JSON file
    with open('video_data.json', 'w') as f:
        json.dump(all_video_data, f, indent=4)

    print("Video data has been successfully fetched and saved to video_data.json.")

if __name__ == "__main__":
    main()
