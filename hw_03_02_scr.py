import requests as rqsts
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def scrape_quotes():
    quotes = []
    authors = []
    visited_authors = set()
    next_page = "/page/1/"
    
    while next_page:
        response = rqsts.get(BASE_URL + next_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for quote_block in soup.select('.quote'):
            text = quote_block.select_one('.text').get_text(strip=True)
            author = quote_block.select_one('.author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote_block.select('.tags .tag')]
            
            quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })
            
            if author not in visited_authors:
                visited_authors.add(author)
                author_url = quote_block.select_one('span a')['href']
                author_response = rqsts.get(BASE_URL + author_url)
                author_soup = BeautifulSoup(author_response.text, 'html.parser')
                
                fullname = author_soup.select_one('.author-title').get_text(strip=True)
                born_date = author_soup.select_one('.author-born-date').get_text(strip=True)
                born_location = author_soup.select_one('.author-born-location').get_text(strip=True)
                description = author_soup.select_one('.author-description').get_text(strip=True)
                
                authors.append({
                    "fullname": fullname,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description
                })
        
        next_page_link = soup.select_one('.next a')
        next_page = next_page_link['href'] if next_page_link else None
    
    return quotes, authors

# Скрапінг
quotes, authors = scrape_quotes()

# Збереження у JSON
with open('qoutes.json', 'w', encoding='utf-8') as q_file:
    json.dump(quotes, q_file, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as a_file:
    json.dump(authors, a_file, ensure_ascii=False, indent=4)
