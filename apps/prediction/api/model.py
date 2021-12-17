import csv
import os

import torch
from django.conf import settings
from sentence_transformers import CrossEncoder, SentenceTransformer, util

TOP_RESULTS = 100
RERANKED_RESULTS = 5

passages = []
passages_cache = []

ss_encoder = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
ss_encoder.max_seq_length = 256  # 512
cross_encoder = CrossEncoder(
    'cross-encoder/msmarco-MiniLM-L12-en-de-v1', max_length=512
)

# подготовка датасета
path = os.path.join(settings.SITE_ROOT, 'export_data', 'passages.csv')
with open(path, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        # post_id - идентификатор вопроса
        # идентификатор ответа на вопрос
        # sentence_type: тип текста, принимает значения:
        #   3 - заголовок вопроса,
        #   2 - тело запроса,
        #   1 - тело ответа
        # passage - собственно текст
        post_id, answer_id, sentence_type, passage = row

        i += 1
        if i % 100000 == 0:
            print(
                f'{(str(i) + ")").ljust(12)}'
                f'{str(post_id).ljust(12)}'
                f'{str(answer_id).ljust(12)}'
                f'{sentence_type}: '
                f'{passage[:50]}'
            )

        passages.append(passage)
        # для того чтобы восстановить исходные идентификаторы и источники
        passages_cache.append({
            'post_id': post_id,
            'answer_id': answer_id,
            'sentence_type': sentence_type
        })

# corpus_embeddings = ss_encoder.encode(
#     passages, convert_to_tensor=True, show_progress_bar=True
# )

# загружу заранее приготовленный тензор с эмбеддингами датасета
corpus_path = os.path.join(
    settings.SITE_ROOT, 'export_data', 'corpus_embeddings.pt'
)
corpus_embeddings = torch.load(corpus_path, map_location='cpu')


def predict(query, ss_results=TOP_RESULTS, reranked_results=RERANKED_RESULTS):
    # Кодируем запрос использую кодировщик SentenceTransformer
    query_embedding = ss_encoder.encode(query, convert_to_tensor=True)
    # query_embedding = query_embedding.cuda()
    hits = util.semantic_search(
        query_embedding, corpus_embeddings, top_k=ss_results
    )
    hits = hits[0]  # Получаем результаты по первому запросу
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)

    cross_pairs = [(query, passages[hit['corpus_id']]) for hit in hits]
    cross_scores = cross_encoder.predict(cross_pairs)

    for idx in range(len(cross_scores)):
        hits[idx]['cross_score'] = cross_scores[idx]

    hits = sorted(hits, key=lambda x: x['cross_score'], reverse=True)
    return_hits = hits[0:reranked_results]
    for hit in return_hits:
        hit.update(**passages_cache[hit['corpus_id']])
        hit['passage'] = passages[hit['corpus_id']]
        del hit['corpus_id']
    return return_hits
