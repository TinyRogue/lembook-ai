import logging

import gensim
from utils import load_data

DATA_PATH = 'nanoDB.processed.json'
BASE_MODEL = 'models/doc2vec.model4'


def prepare_documents():
    ids, descriptions = load_data(DATA_PATH)
    return [gensim.models.doc2vec.TaggedDocument(tokens, [i]) for tokens, i in zip(descriptions, ids)]


def get_model():
    return gensim.models.doc2vec.Doc2Vec(vector_size=400, min_count=2, epochs=20, dm=1, dbow_words=1, dm_concat=1, window=7)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    docs = prepare_documents()
    model = get_model()
    model.build_vocab(docs)
    model.train(docs, total_examples=model.corpus_count, epochs=model.epochs)
    model.save(BASE_MODEL)
