import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import numpy as np
import seaborn as sns
from collections import defaultdict
from matplotlib import pyplot as plt

def _decode_title(title):
    return title.replace('.txt', '').split('_')

def get_speeches():
    filenames = []
    speech_contents = []
    for filename in os.listdir("."):
        if filename.endswith(".txt"):
            filenames.append(filename)
            f = open(filename, encoding='utf-8')
            text = f.read()
            speech_contents.append(text)
    return speech_contents, filenames

def preproc_word(s):
    invalid_characters = '[]{}'
    for c in invalid_characters:
        s = s.replace(c, '')
    return PorterStemmer().stem(s)

def _get_candidate_rankings(filename):
    speeches, names = get_speeches()
    speeches_lower_stemmed = [s.lower() for s in speeches]
    speech_vectors = TfidfVectorizer(stop_words='english',
                                     preprocessor=preproc_word,
                                     ngram_range=(1, 2)).fit_transform(speeches_lower_stemmed)
    speech_lookup = {n : sv.toarray().flatten() for n, sv in zip(names, speech_vectors)}
    target_candidate = speech_lookup[filename]
    results = [(np.dot(target_candidate, speech_lookup[n]), n) for n in names]
    return sorted(results, reverse=True)

def get_trump_rankings():
    return _get_candidate_rankings('Donald J. Trump_2016_Republican.txt')

def get_clinton_rankings():
    return _get_candidate_rankings('Hillary Clinton_2016_Democratic.txt')

def plot_distances_over_time():
    speeches, names = get_speeches()
    speeches_lower_stemmed = [s.lower() for s in speeches]
    speech_vectors = TfidfVectorizer(stop_words='english',
                                     preprocessor=lambda s: PorterStemmer().stem(s),
                                     ngram_range=(1, 3)).fit_transform(speeches_lower_stemmed)
    speech_vectors = [sv.toarray().flatten() for sv in speech_vectors]
    pairs = defaultdict(list)
    for name, vector in zip(names, speech_vectors):
        nominee, year, party = _decode_title(name)
        pairs[year].append(vector)
    years, similarities = [], []
    for year in sorted(pairs.keys()):
        if len(pairs[year]) == 2:
            similarities.append(np.dot(*pairs[year]))
            years.append(year)
    plt.plot(years, similarities, marker='o')
    plt.show()

def display_rankings(rankings):
    color_lookup = {'Democratic': 'blue', 'Republican':'red'}
    tup, *rankings = rankings
    score, filename = tup
    target_name, target_year, target_party = _decode_title(filename)
    print(target_name, ' MOST SIMILAR:')
    names = []
    scores = []
    for score, filename in rankings[1:]:
        name, year, party = _decode_title(filename)
        print(name, score)
        if party == target_party:
            names.append('{0}, {1}'.format(name, year))
            scores.append(score)
    names = list(reversed(names[:10]))
    scores = list(reversed(scores[:10]))
    plt.title('TF-IDF similarity of {0} to past {1} nomination speeches'.format(target_name, target_party), size=22)
    plt.barh(range(len(names)), scores, align='center', color=color_lookup[target_party])
    plt.yticks(range(len(names)), names, size=20)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    display_rankings(get_trump_rankings())
    display_rankings(get_clinton_rankings())
    plot_distances_over_time()