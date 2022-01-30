import gensim

from utils import load_data

DATA_PATH = 'nanoDB.processed.json'
BASE_MODEL = 'models/doc2vec.model4'

if __name__ == '__main__':
    ids, docs = load_data(DATA_PATH)
    _, d = load_data('nanoDB.json')
    model = gensim.models.doc2vec.Doc2Vec.load(BASE_MODEL)
    vec = model.infer_vector(["kailyn", "wilde", "fortune", "telling", "aunt", "tilly", "special", "magic", "power", "fritz", "bit", "lately", "friend", "husband", "murdered", "kailyn", "aunt", "tilly", "find", "body", "kailyn", "decides", "work", "killed", "jim", "bit", "amateur", "sleuthing", "add", "legendary", "merlin", "suddenly", "time", "travel", "life", "ghost", "kailyn", "grandmother", "mother", "new", "boyfriend", "number", "demanding", "cat", "gentle", "humorous", "slightly", "paranormal", "cozy"])
    sims = model.dv.most_similar([vec], topn=10)
    print('Similar')
    for sim in sims:
        i = ids.index(sim[0])
        print(f'{d[i]} for {sim[1] * 100}% sure')
