"""
Retriever: loads data/docs_content.json, splits content into chunks, builds a TF-IDF index,
and provides a function `get_best_response(query, top_k=1)` that returns best matching segments.
"""

import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DATA_FILE = os.path.join('data', 'docs_content.json')


def chunk_text(text, max_len=800):
    # Naive chunker: split by paragraph and join until threshold
    paras = re.split(r'\n{2,}|\n', text)
    chunks = []
    cur = ''

    for p in paras:
        p = p.strip()
        if not p:
            continue
        if len(cur) + len(p) <= max_len:
            cur = cur + '\n\n' + p if cur else p
        else:
            chunks.append(cur)
            cur = p

    if cur:
        chunks.append(cur)
    return chunks


class Retriever:
    def __init__(self, data_file=DATA_FILE):
        if not os.path.exists(data_file):
            raise FileNotFoundError(f'{data_file} not found. Run scraper first or use provided sample')

        with open(data_file, 'r', encoding='utf-8') as f:
            pages = json.load(f)

        self.segments = []  # list of dicts {url, title, text}
        for p in pages:
            chunks = chunk_text(p.get('content', ''))
            for c in chunks:
                self.segments.append({
                    'url': p.get('url'),
                    'title': p.get('title'),
                    'text': c
                })

        texts = [s['text'] for s in self.segments]
        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9)
        if texts:
            self.tfidf = self.vectorizer.fit_transform(texts)
        else:
            self.tfidf = None

    def get_best_response(self, query, top_k=1):
        if self.tfidf is None or self.tfidf.shape[0] == 0:
            return []

        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.tfidf)[0]
        top_idx = np.argsort(sims)[::-1][:top_k]

        results = []
        for idx in top_idx:
            seg = self.segments[idx]
            score = float(sims[idx])
            results.append({
                'title': seg['title'],
                'url': seg['url'],
                'text': seg['text'][:800] + ('...' if len(seg['text']) > 800 else ''),
                'score': round(score, 4)
            })

        return results
