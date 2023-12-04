import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_parent(parent: list, a: int):
    if parent[a] == a:
        return parent[a]

    parent[a] = find_parent(parent, parent[a])
    return parent[a]


def union_parent(parent: list, a: int, b: int):
    parent_a = find_parent(parent, a)
    parent_b = find_parent(parent, b)

    if parent_a < parent_b:
        parent[parent_a] = parent_b
    else:
        parent[parent_b] = parent_a


def calculate_similarity(path: str):
    documents = []
    with open(path, 'r', encoding='UTF8') as file:
        text_data = json.load(file)
    for news in text_data:
        documents.append((news["content"]))

    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 여러 문서 간의 코사인 유사도 계산
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    return cosine_sim


def clustering_news(path: str):
    cosine_sim = calculate_similarity(path)
    parent = [x for x in range(len(cosine_sim))]

    for i, metrix in enumerate(cosine_sim):
        for j, val in enumerate(metrix):
            if val >= 0.7:
                union_parent(parent, i, j)

    d = dict()
    for i in range(len(parent)):
        k = find_parent(parent, i)
        if k in d:
            d[k].append(i)
        else:
            d[k] = [i]

    data = sorted(list(d.items()), key=lambda x: len(x[1]), reverse=True)
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    path_split = path.split("/")[3].split("-")
    category = path_split[0]
    date = path_split[1].split(".")[0]
    new_path = f"./data/cluster/{category}-{date}.json"
    with open(new_path, 'w', encoding='utf-8') as file:
        file.write(json_data)


if __name__ == "__main__":
    categories = ["society", "politics", "economic"]
    date = "20231203"

    for category in categories:
        path = f"./data/news/{category}-{date}.json"
        clustering_news(path=path)
