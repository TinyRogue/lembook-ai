import json
import string

import contractions
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from utils import load_data

LEMMA_THING = WordNetLemmatizer()
DATA_PATH = 'nanoDB.json'


if __name__ == '__main__':
    print('Loading the data...')
    tags, descriptions = load_data(DATA_PATH)

    print('Expanding...')
    expanded = [contractions.fix(d) for d in descriptions]

    print('Processing to lowercase...')
    lowercase = [d.lower() for d in expanded]

    print('Tokenizing...')
    tokenized = [nltk.tokenize.word_tokenize(d) for d in lowercase]

    print('Removing stopwords...')
    stopwords = ["'s", 'http', 'https', *stopwords.words('english')]
    for i, sentence in enumerate(tokenized):
        tokenized[i] = [word for word in sentence if word not in stopwords]

    print('Removing punctuation...')
    punctuation = ['...', '``', "''", '--', '....', *string.punctuation]
    for i, sentence in enumerate(tokenized):
        tokenized[i] = [word for word in sentence if word not in punctuation]

    print('Lemmatizing...')
    for i, sentence in enumerate(tokenized):
        tokenized[i] = [LEMMA_THING.lemmatize(word) for word in sentence]

    processed = [{'uid': uid, 'description': desc} for uid, desc in zip(tags, tokenized)]
    with open('nanoDB.processed.json', 'w') as outfile:
        json.dump(processed, outfile)

    print('All things done. Goodbye!')
