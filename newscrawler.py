import json

import requests
from bs4 import BeautifulSoup


def crawl_daum_news(category: str, date: str):
    url = "https://news.daum.net/breakingnews/" + category
    header = {"user-agent": "Mozilla/5.0"}

    page = 1
    cnt = 0
    result = []

    while True:
        params = {
            'page': page,
            'regDate': date
        }

        response = requests.get(url, params=params, headers=header)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        news = (soup.find("ul", {"class": "list_news2 list_allnews"})
                .find_all("strong", {"class": "tit_thumb"}))

        current_page = soup.find("em", {"class": "num_page"}).text
        if page != int(current_page[7:]):
            break

        print(f"DEBUG  {category}-{date} page: {page}")

        for idx, item in enumerate(news):
            link = item.find('a')
            info = item.find('span', {"class": "info_news"})

            href = link.get("href")
            text = link.get_text(strip=True)
            company = info.get_text(strip=True)[:-6]
            time_info = info.find("span", {"class": "info_time"}).get_text(strip=True)

            content = crawl_news_paragraph(href)

            if len(content) >= 300:
                result.append({
                    "id": cnt,
                    "title": text,
                    "url": href,
                    "company": company,
                    "time": time_info,
                    "content": content,
                })
                cnt += 1
        page += 1

        # time.sleep(0.001)

    json_data = json.dumps(result, ensure_ascii=False, indent=4)
    with open(f'./data/news/{category}-{date}.json', 'w', encoding='utf-8') as file:
        file.write(json_data)


def crawl_news_paragraph(url: str):
    header = {"user-agent": "Mozilla/5.0"}

    response = requests.get(url, headers=header)
    html = response.text
    soup2 = BeautifulSoup(html, 'html.parser')
    p_tags = soup2.find("article").find("section").find_all("p")
    paragraph = "\n".join(map(lambda x: x.get_text(), p_tags))

    return paragraph


if __name__ == "__main__":
    categories = ["society", "politics", "economic"]
    date = "20231203"
    for category in categories:
        crawl_daum_news(category=category, date=date)
