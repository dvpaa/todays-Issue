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


documents = []
with open('./data/news-politics-20231130-text.json', 'r') as file:
    text_data = json.load(file)
for news in text_data:
    documents.append((news["text"]))

# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)



# 여러 문서 간의 코사인 유사도 계산
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

parent = [x for x in range(len(cosine_sim))]

for i, metrix in enumerate(cosine_sim):
    for j, val in enumerate(metrix):
        if val >= 0.7:
            print(f'idx: {i},{j}  val: {val}')
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

with open(f'result.json', 'w', encoding='utf-8') as file:
    file.write(json_data)
