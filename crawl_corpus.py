from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
# from unidecode import unidecode

START_URL = 'http://www.presidency.ucsb.edu/nomination.php'



def reduce_whitespace(s):
    s = s.replace('\n', ' ')
    s = s.replace('\r', ' ')
    return re.sub(' +', ' ', s).strip()

# Yes I know this code is a bunch of ad-hoc magic number brittle crap, I'm sorry Uncle Bob

def extract_data_from_tds(tds):
    text = [td.text for td in tds]
    formatted_text = [reduce_whitespace(t) for t in text]
    if hasattr(tds[0].contents[0], 'get'):
        link = tds[0].contents[0].get('href')
    else:
        link = 'Not yet available'
    name = formatted_text[0]
    year = formatted_text[1][-4:]
    return name, link, year


def get_year_rows():
    html_doc = urlopen(START_URL).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    current_party = None
    data = []
    for row in soup.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) == 1 and 'Party' in tds[0].text:
            current_party = reduce_whitespace(tds[0].text)[:-5].strip()
        if len(tds) == 7:
            name, link, year = extract_data_from_tds(tds)
            data.append((name, link, year, current_party))
    return data

def get_speech_text(speech_url):
    html_doc = urlopen(speech_url).read()
    speech_soup = BeautifulSoup(html_doc, 'html.parser')
    for span in speech_soup.find_all('span'):
        if span.get('class') == ['displaytext']:
            return span.text

data = get_year_rows()[1:] # Drop first row until Clinton's speech is out

for name, link, year, party in data:
    speech_text = get_speech_text(link)
    filename = '{0}_{1}_{2}.txt'.format(name, year, party)
    f = open(filename, 'w', encoding='utf-8')
    f.write(speech_text)
    f.close()