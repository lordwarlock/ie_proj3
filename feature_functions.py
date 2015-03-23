import re
import inflect

def get_feature_functions():
    return [distance]

def distance(coref,corpus):
    """number of word between two mentions"""
    return coref.second.start-coref.first.end

def entity_type(coref,corpus):
    return coref.first.ne+'-'+coref.second.ne

def hint_word_detection(coref,corpus,token_distance = 3,hint_words = ['is','are','was','were','be']):
    """if two mentions are linked by certain word"""
    if(coref.first.sent != coref.second.sent): return False
    if ((coref.second.start - coref.first.start) > token_distance): return False
    between_word_list = []
    document = coref.document
    sentence = corpus.postagged_data[document][coref.first.sent].tokens
    for i in range(coref.first.start,coref.second.end):
        if (sentence[i][0] in hint_words):
            print coref.first.word,coref.first.end, coref.second.word,coref.second.start
            print sentence[coref.first.start:coref.second.end]
            return True

    return False
        
def hint_who_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['who','which'],token_distance=5)

if __name__ == '__main__':
    from data_reader import *
    from feature_extraction import FeatureExtraction
    from build_corpus import BuildCorpus
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.test(DataSet(r"./project2/data/coref-trainset.gold"),appositive)
