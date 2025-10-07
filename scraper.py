import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# --- Configuration ---
START_URLS = ["https://docs.capillarytech.com/"]
DATA_FILE = "data/docs_content.json"
MAX_PAGES = 30
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CapillaryBot/1.0)"}


# --- Helper functions ---
def same_domain(url, domain):
    """Check if a URL belongs to the same domain."""
    return urlparse(url).netloc == domain


def normalize_url(base, link):
    """Convert relative links to absolute ones."""
    return urljoin(base, link)


def extract_text_from_soup(soup):
    """Extract readable text content from HTML."""
    for script in soup(["script", "style", "noscript"]):
        script.extract()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


# --- Main crawler ---
def crawl(start_urls, max_pages=MAX_PAGES):
    domain = urlparse(start_urls[0]).netloc
    to_visit = list(start_urls)
    visited = set()
    results = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code != 200:
                visited.add(url)
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else url
            content = extract_text_from_soup(soup)

            if content and len(content) > 50:
                results.append({
                    'url': url,
                    'title': title,
                    'content': content
                })

            visited.add(url)

            # Find internal links
            for a in soup.find_all('a', href=True):
                href = a['href']
                full = normalize_url(url, href)
                if full in visited:
                    continue
                if same_domain(full, domain):
                    # prune fragments and mailto
                    if full.startswith('mailto:'):
                        continue
                    if '#' in full:
                        full = full.split('#')[0]
                    if full not in to_visit:
                        to_visit.append(full)

        except Exception as e:
            print(f"Error crawling {url}: {e}")
            visited.add(url)
            continue

    return results


# --- Run the crawler ---
if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    print('Crawling start URLs...')
    items = crawl(START_URLS)
    print(f'Scraped {len(items)} pages')

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print('Saved to', DATA_FILE)
