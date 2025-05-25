import os
import sys
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import tldextract
import argparse
import sqlite3

console = Console()
EXTENSIONS = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.sql', '.csv', '.json')
VISITED_URLS = set()

def setup_db():
    conn = sqlite3.connect("foxchief_results.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  url TEXT,
                  file_type TEXT,
                  size_kb REAL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

def is_valid_url(base_netloc, url):
    parsed = urlparse(url)
    return parsed.netloc == base_netloc and parsed.scheme in ['http', 'https']

def get_size(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        size = int(response.headers.get('Content-Length', 0)) / 1024
        return round(size, 2)
    except:
        return "Unknown"

def save_to_db_single(url, ftype, size):
    conn = setup_db()
    c = conn.cursor()
    c.execute("INSERT INTO files (url, file_type, size_kb) VALUES (?, ?, ?)", (url, ftype, size))
    conn.commit()
    conn.close()

def crawl(base_url):
    domain = urlparse(base_url).netloc
    queue = [base_url]
    found_files = []

    while queue:
        current_url = queue.pop(0)
        if current_url in VISITED_URLS:
            continue

        console.print(f"[cyan][CRAWL][/cyan] {current_url}")
        VISITED_URLS.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                new_url = urljoin(current_url, link['href'])
                if not is_valid_url(domain, new_url):
                    continue

                if new_url.endswith(EXTENSIONS):
                    file_type = os.path.splitext(new_url)[1].lower()
                    size = get_size(new_url)
                    console.print(f"[green][FOUND][/green] {new_url} ([yellow]{size} KB[/yellow])")
                    found_files.append((new_url, file_type, size))
                    save_to_db_single(new_url, file_type, size)
                elif new_url not in VISITED_URLS and new_url not in queue:
                    queue.append(new_url)

        except Exception as e:
            pass

    return found_files

def main(target_url):
    console.print(Panel("[bold blue]🦊 FoxChief - Advanced File Hunter 🦊\nTarget: [/bold blue]" + target_url, expand=False))

    start_time = time.time()
    results = crawl(target_url)

    console.print(f"\n✅ Total files found: {len(results)} | Time taken: {round(time.time() - start_time, 2)} seconds")
    console.print("[blue]📄 Results saved to: foxchief_results.db[/blue]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🦊 FoxChief - File Hunter & Crawler")
    parser.add_argument("url", help="Target URL to scan")
    args = parser.parse_args()
    main(args.url)
