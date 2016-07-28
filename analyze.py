import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import numpy as np

def get_speeches():
    filenames = []
    speech_contents = []
    for filename in os.listdir("."):
        if filename.endswith(".txt"):
            filenames.append(filename)
            f = open(filename)
            text = f.read()
            speech_contents.append(text)
    return speech_contents, filenames

def get_trump_rankings():
    speeches, names = get_speeches()
    speeches_lower = [s.lower() for s in speeches]
    speech_vectors = TfidfVectorizer(stop_words='english').fit_transform(speeches_lower)
    speech_lookup = {n : sv.toarray().flatten() for n, sv in zip(names, speech_vectors)}
    the_donald = speech_lookup['Donald J. Trump_2016_Republican.txt']
    results = [(np.dot(the_donald, speech_lookup[n]), n) for n in names if n != 'Donald Trump']
    print(sorted(results, reverse=True))

if __name__ == '__main__':
    get_trump_rankings()
