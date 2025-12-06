import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class HeadlineScraper:
    def __init__(self, user_agent=None):
        """Initialize the scraper with optional custom user agent."""
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_headlines(self, url, tag='h2', class_name=None, limit=10):
        """
        Scrape headlines from a given URL.
        
        Args:
            url: The website URL to scrape
            tag: HTML tag to look for (default: 'h2')
            class_name: Optional CSS class to filter by
            limit: Maximum number of headlines to return
            
        Returns:
            List of dictionaries containing headline text and links
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # Find all matching tags
            if class_name:
                elements = soup.find_all(tag, class_=class_name, limit=limit)
            else:
                elements = soup.find_all(tag, limit=limit)
            
            for elem in elements:
                # Extract text
                text = elem.get_text(strip=True)
                
                # Try to find link
                link = None
                a_tag = elem.find('a') or elem.find_parent('a')
                if a_tag and a_tag.get('href'):
                    link = urljoin(url, a_tag['href'])
                
                if text:  # Only add if there's actual text
                    headlines.append({
                        'text': text,
                        'link': link
                    })
            
            return headlines
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return []
    
    def scrape_multiple_tags(self, url, tags=['h1', 'h2', 'h3'], limit=15):
        """
        Scrape headlines using multiple HTML tags.
        
        Args:
            url: The website URL to scrape
            tags: List of HTML tags to search
            limit: Maximum number of headlines to return
            
        Returns:
            List of dictionaries containing headline text and links
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            for tag in tags:
                elements = soup.find_all(tag)
                for elem in elements:
                    text = elem.get_text(strip=True)
                    
                    link = None
                    a_tag = elem.find('a') or elem.find_parent('a')
                    if a_tag and a_tag.get('href'):
                        link = urljoin(url, a_tag['href'])
                    
                    if text and len(text) > 10:  # Filter very short text
                        headlines.append({
                            'text': text,
                            'link': link,
                            'tag': tag
                        })
                    
                    if len(headlines) >= limit:
                        break
                
                if len(headlines) >= limit:
                    break
            
            return headlines
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return []


def main():
    """Example usage of the HeadlineScraper."""
    scraper = HeadlineScraper()
    
    # Example: BBC News (adjust tags/classes based on actual site structure)
    print("=" * 60)
    print("SCRAPING HEADLINES")
    print("=" * 60)
    
    url = "https://news.ycombinator.com"  # Example site
    print(f"\nFetching from: {url}\n")
    
    headlines = scraper.scrape_multiple_tags(url, tags=['a'], limit=10)
    
    if headlines:
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline['text']}")
            if headline['link']:
                print(f"   Link: {headline['link']}")
            print()
    else:
        print("No headlines found. Try adjusting the tags or class names.")
    
    # Example with specific tag and class
    print("\n" + "=" * 60)
    print("CUSTOM TAG SEARCH")
    print("=" * 60)
    
    # Adjust these parameters based on your target website
    custom_headlines = scraper.scrape_headlines(
        url=url,
        tag='a',
        class_name='titleline',  # Example class name
        limit=5
    )
    
    if custom_headlines:
        for i, headline in enumerate(custom_headlines, 1):
            print(f"{i}. {headline['text']}")
            if headline['link']:
                print(f"   Link: {headline['link']}")
            print()


if __name__ == "__main__":
    main()