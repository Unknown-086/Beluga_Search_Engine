import time

from src.CrawlingWebLinks.CrawlUrl import crawl_url, scrape_website

# usage

url = "https://lms.nust.edu.pk/portal/mod/assign/view.php?id=1091952&action=view"

start = time.time()
print(crawl_url(url, 'all'))
end = time.time()
print(f"Time taken: {end - start:.6f} seconds")

start = time.time()
print(scrape_website(url))
end = time.time()
print(f"Time taken: {end - start:.6f} seconds")