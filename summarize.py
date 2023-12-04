# -*- coding: utf-8 -*-
import json

from summarizer import Summarizer


def summarize_news(article_text):
    summarizer = Summarizer()
    summary = summarizer(article_text)

    return summary


if __name__ == "__main__":
    categories = ["society", "politics", "economic"]
    date = "20231203"
    result = {}
    for category in categories:
        with open(f"./data/cluster/{category}-{date}.json", 'r', encoding="UTF8") as file:
            unions = json.load(file)

        with open(f"./data/news/{category}-{date}.json", 'r', encoding="UTF8") as file:
            news_articles = json.load(file)

        result[category] = []
        for idx, union in enumerate(unions[:10]):

            news_article = news_articles[union[1][len(union[1])//2]]["content"]
            result[category].append({
                "rank": idx,
                "summary": summarize_news(news_article),
            })

    json_data = json.dumps(result, ensure_ascii=False, indent=4)
    with open(f"./data/summary/{date}-topic.json", "w", encoding='utf-8') as file:
        file.write(json_data)
