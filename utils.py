import json
from enum import Enum

INVALID_UID = ['5UenQcZ9C3lZcxLlkpZS0']


class BookProps(Enum):
    title = 'title'
    authors = 'authors'
    genres = 'genres'
    cover = 'cover'
    description = 'description'
    uid = 'uid'


def load_data(path):
    with open(path) as f:
        raw_data = json.load(f)
        raw_data = [d for d in raw_data if d[BookProps.uid.value] not in INVALID_UID]
        return [x[BookProps.uid.value] for x in raw_data], [x[BookProps.description.value] for x in raw_data]
