// Function to fetch video data from video_data.json
function fetchVideoData() {
    fetch('video_data.json')
        .then(response => response.json())
        .then(data => displayVideos(data))
        .catch(error => console.error('Error fetching video data:', error));
}

// Function to display video data on the page
function displayVideos(data) {
    const videoList = document.getElementById('video-list');

    // Clear existing content
    videoList.innerHTML = '';

    // Iterate over the video data and create elements for each video
    for (const folderId in data) {
        const videoInfo = data[folderId];

        const videoItem = document.createElement('div');
        videoItem.classList.add('video-item');

        // Create the thumbnail image
        const thumbnail = document.createElement('img');
        thumbnail.src = videoInfo.thumbnail_url;
        thumbnail.alt = `Thumbnail for ${folderId}`;
        thumbnail.classList.add('thumbnail');

        // Create the video title (folder ID)
        const title = document.createElement('h3');
        title.textContent = folderId;

        // Create the video element
        const videoLink = document.createElement('a');
        videoLink.href = videoInfo.video_url;
        videoLink.textContent = 'Watch Video';
        videoLink.target = '_blank';

        // Append elements to video item
        videoItem.appendChild(thumbnail);
        videoItem.appendChild(title);
        videoItem.appendChild(videoLink);

        // Append the video item to the list
        videoList.appendChild(videoItem);
    }
}

// Run the fetch function when the page loads
document.addEventListener('DOMContentLoaded', fetchVideoData);
