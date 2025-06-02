import requests
from bs4 import BeautifulSoup
import time

# Входные данные
url1 = "https://en.wikipedia.org/wiki/Six_degrees_of_separation"
url2 = "https://en.wikipedia.org/wiki/American_Broadcasting_Company"
rate_limit = 10

def get_wikipedia_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return {f"https://en.wikipedia.org{a['href']}"
                for a in soup.select('div.mw-parser-output a[href^="/wiki/"]')
                if ":" not in a['href']}
    except Exception as e:
        return set()

def find_path(start_url, target_url, rate_limit):
    visited = set()
    stack = [(start_url, [start_url])]
    requests_made = 0

    while stack:
        current_url, path = stack.pop()

        if current_url == target_url:
            return path
        if len(path) >= 5 or current_url in visited:
            continue

        visited.add(current_url)
        links = get_wikipedia_links(current_url)
        requests_made += 1

        if requests_made >= rate_limit:
            time.sleep(1)
            requests_made = 0

        for link in links:
            if link not in visited:
                stack.append((link, path + [link]))

    return None

def main(url1, url2, rate_limit):
    for start_url, target_url in [(url1, url2), (url2, url1)]:
        path = find_path(start_url, target_url, rate_limit)
        if path:
            print(f"Путь от {start_url} к {target_url}: {' -> '.join(path)}")
        else:
            print(f"Путь от {start_url} к {target_url} не найден за 5 шагов.")

main(url1, url2, rate_limit)