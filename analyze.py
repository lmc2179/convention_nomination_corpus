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
                                     preprocessor=preproc_word).fit_transform(speeches_lower_stemmed)
    speech_lookup = {n : sv.toarray().flatten() for n, sv in zip(names, speech_vectors)}
    target_candidate = speech_lookup[filename]
    results = [(np.dot(target_candidate, speech_lookup[n]), n) for n in names]
    print(sorted(results, reverse=True))

def get_trump_rankings():
    return _get_candidate_rankings('Donald J. Trump_2016_Republican.txt')

def get_clinton_rankings():
    return _get_candidate_rankings('Hillary Clinton_2016_Democratic.txt')

def plot_distances_over_time():
    speeches, names = get_speeches()
    speeches_lower_stemmed = [s.lower() for s in speeches]
    speech_vectors = TfidfVectorizer(stop_words='english',
                                     preprocessor=lambda s: PorterStemmer().stem(s)).fit_transform(speeches_lower_stemmed)
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

if __name__ == '__main__':
    get_trump_rankings()
    get_clinton_rankings()
    # plot_distances_over_time()