import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.shl.com"


# Collect all assessment links (pagination)
assessment_links = set()
start = 0
PAGE_SIZE = 12

while True:
    page_url = f"https://www.shl.com/products/product-catalog/?start={start}&type=1"
    print(f"Fetching catalog page: {page_url}")

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")
    found_on_page = 0

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href_lower = href.lower()

        if (
            "/products/product-catalog/view/" in href_lower
            and "solution" not in href_lower
        ):
            full_url = href if href.startswith("http") else BASE_URL + href
            assessment_links.add(full_url)
            found_on_page += 1

    if found_on_page == 0:
        break

    start += PAGE_SIZE
    time.sleep(1)

print(f"Total assessment links collected: {len(assessment_links)}")


# STEP 2: Visit each assessment page and extract details
assessments_data = []

for url in assessment_links:
    print(f"Scraping assessment: {url}")

    page = requests.get(url)
    page_soup = BeautifulSoup(page.text, "html.parser")

    title_tag = page_soup.find("h1")
    name = title_tag.text.strip() if title_tag else ""

    description = ""
    desc_div = page_soup.find("div", class_="product-description")
    if desc_div:
        description = desc_div.text.strip()

    assessments_data.append({
        "name": name,
        "url": url,
        "description": description
    })

    time.sleep(1)

print(f"Total assessments scraped: {len(assessments_data)}")


# STEP 3: Save to CSV
df = pd.DataFrame(assessments_data)
df.to_csv("data/shl_assessments_raw.csv", index=False)

print("Scraping finished. File saved.")
