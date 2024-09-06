import json
import prettyprint as pp
import urllib.request
import os
from urllib.parse import urlsplit


with open('311_url_all.json', 'r') as file:
	data = json.load(file)

#extract all media_urls_data 

media_urls = [item['media_url'] for item in data]
service_request_ids = [item['service_request_id'] for item in data]

# Directory to save images

save_directory = 'images'
os.makedirs(save_directory, exist_ok=True)  # Create directory if it doesn't exist

# Loop through each URL, service_request_id
for url, service_request_id in zip(media_urls, service_request_ids):
    try:
        # Open the URL and read the image data
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        
        # Extract the file extension from the URL
        path = urlsplit(url).path
        file_extension = os.path.splitext(path)[1]  # Extract file extension from URL path
        if not file_extension:
            file_extension = '.jpg'  # Default extension if none found
        
        # Construct the filename using the service request id/file extension
        filename = os.path.join(save_directory, f'{service_request_id}{file_extension}')
        
        # Write the image data to a file
        with open(filename, 'wb') as file:
            file.write(image_data)
        
        print(f"Image saved to {filename}")
    
    except urllib.error.HTTPError as e:
        # Handle HTTP errors
        print(f"HTTPError: {e.code} - {e.reason} for URL: {url}")
    
    except urllib.error.URLError as e:
        # Handle URL errors
        print(f"URLError: {e.reason} for URL: {url}")
    
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e} for URL: {url}")