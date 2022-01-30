import math
import os
import sys
import certifi
import gensim
from decouple import config
from dotenv import load_dotenv
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from waitress import serve
from utils import load_data

PASS_KEY = config('PASS_KEY')
DB_NAME = 'TheDB'
BOOKS_COLLECTION_NAME = 'books'
USERS_COLLECTION_NAME = 'users'
DATA_PATH = 'nanoDB.processed.json'
BASE_MODEL = 'models/doc2vec.model4'

app = Flask(__name__)
CORS(app)
dbx = None
books_collection = None
users_collection = None
book_ids = None
documents = None
model = None


def get_proposed_books(number, uids):
    buckets_count = len(uids)
    big_bucket_capacity = int(math.ceil(number / buckets_count))
    big_buckets_count = number % buckets_count

    if big_buckets_count == 0:
        big_bucket_capacity += 1

    recommendation_uids = set()
    for i in range(buckets_count):
        capacity = big_bucket_capacity
        if i >= big_buckets_count:
            capacity -= 1
        document_data = documents[ids.index(uids[i])]
        vec = model.infer_vector(document_data)
        sims = model.dv.most_similar([vec], topn=capacity)
        for sim in sims:
            recommendation_uids.add(sim[0])

    return recommendation_uids - set(uids)


@app.route("/similar-books/<user_uid>")
def find_similar_books(user_uid):
    print('Find similar books request.')
    if request.args.get('key') != PASS_KEY:
        print('Access denied: Invalid or empty pass key.')
        return abort(403, description="Invalid or empty pass key.")
    books_number = request.args.get('books')
    if books_number is None or not books_number.isdigit() or not(1 < int(books_number) < 100):
        print('Bad request: Books number must be positive integer, not higher than 100.')
        return abort(400, description="Books number must be positive integer, not higher than 100.")
    if user_uid is None:
        print("Bad request: User's UID cannot be null.")
        return abort(400, description="User's UID cannot be null.")

    print('Looking for a user...')
    user = users_collection.find_one({'uid': user_uid})
    if user is None:
        print("Bad request: No such user.")
        return abort(400, description="No such user!")

    liked_uids = user['likedBooks']
    if liked_uids is None or len(liked_uids) == 0:
        print('Error: user does not like any book. Unable to perform recommendation.')
        return abort(400, description='Error: user does not like any book. Unable to perform recommendation.')

    print('Successful recommendation request. Predicting...')
    return jsonify(list(get_proposed_books(int(books_number), liked_uids)))


if __name__ == '__main__':
    print('Loading the data...')
    ids, documents = load_data(DATA_PATH)
    print('Loading the model...')
    model = gensim.models.doc2vec.Doc2Vec.load(BASE_MODEL)

    print('Loading environment variables...')
    load_dotenv()
    mongo_pass = os.getenv('ATLAS_URI')
    ca = certifi.where()

    print('Connecting to the DB...')
    db_client = MongoClient(mongo_pass, tlsCAFile=ca)
    db = db_client[DB_NAME]
    books_collection = db[BOOKS_COLLECTION_NAME]
    users_collection = db[USERS_COLLECTION_NAME]
    if books_collection is None or users_collection is None:
        print("Could not access collections' descriptors...")
        sys.exit(1)

    print('Starting the server!')
    serve(app)
