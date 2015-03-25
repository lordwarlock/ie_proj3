import re
import inflect

def get_feature_functions():
    return [dist_0,dist_1,dist_4,dist_6,entity_type,
            hint_comma_detection,hint_of_detection,hint_and_detection,
            hint_s_detection,hint_the_detection,hint_from_detection,hint_in_detection,
            hint_at_detection,hint_like_detection,hint_for_detection]

def distance_n(coref,n):
    """number of word between two mentions"""
    diff = coref.second.start-coref.first.end
    return diff<=n

def dist_0(coref,corpus):
    return distance_n(coref,0)
def dist_1(coref,corpus):
    return distance_n(coref,1)
def dist_4(coref,corpus):
    return distance_n(coref,4)
def dist_6(coref,corpus):
    return distance_n(coref,6)

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
            #print coref.first.word,coref.first.end, coref.second.word,coref.second.start
            #print sentence[coref.first.start:coref.second.end]
            return True

    return False

def hint_comma_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = [','],token_distance=6)

def hint_of_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['of'],token_distance=6)

def hint_and_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['and'],token_distance=6)

def hint_s_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ["'s","'"],token_distance=6)

def hint_the_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['the'],token_distance=6)

def hint_from_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['from'],token_distance=6)

def hint_in_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['in'],token_distance=6)

def hint_at_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['at'],token_distance=6)

def hint_like_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['like'],token_distance=6)

def hint_for_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['for'],token_distance=6)

def hint_who_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['who','which'],token_distance=6)

if __name__ == '__main__':
    from data_reader import *
    from feature_extraction import FeatureExtraction
    from build_corpus import BuildCorpus
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.test(DataSet(r"./project2/data/coref-trainset.gold"),appositive)
