from frequent_words import *

def optimize_search(s):
    ''' optimize a search string, removing common words and duplicates '''
    s=s.lower().replace('\n', ' ')
    s=s.replace('.', ' ')
    s=s.replace(',', ' ')
    s=map(lambda x: x.strip(), list(set(s.split(' '))))
    return ' '.join(filter(lambda x: not x in frequentwords, s))
