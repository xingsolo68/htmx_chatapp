import time

import requests
from bs4 import BeautifulSoup


def scrape_flickr(url, max_retries=3, timeout=10):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Image
            image = soup.find('meta', property='og:image')
            image_url = image['content'] if image else None
            
            # Title
            title_tag = soup.find('h1', class_='photo-title')
            title = title_tag.text.strip() if title_tag else None
            
            # Artist
            artist_tag = soup.find('a', class_='owner-name')
            artist = artist_tag.text.strip() if artist_tag else None
            
            return {
                'image': image_url,
                'title': title,
                'artist': artist
            }
        
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait for 2 seconds before retrying
            continue
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    print(f"Failed to scrape after {max_retries} attempts")
    return None     