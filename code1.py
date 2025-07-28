import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/news"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

# BBC uses this class for main headlines (as of now)
headlines = soup.select("h2, h3")

print("Top BBC News Headlines:\n")
count = 0
for tag in headlines:
    text = tag.get_text(strip=True)
    if text and len(text) > 20:  # Filter short irrelevant texts
        count += 1
        print(f"{count}. {text}")
    if count >= 10:
        break
