import re
import inflect

def get_feature_functions():
    return [dist_0,dist_1,dist_4,dist_6,entity_type,tree_height,
            hint_comma_detection,hint_of_detection,hint_and_detection,
            hint_s_detection,hint_the_detection,hint_from_detection,hint_in_detection,
            hint_at_detection,hint_like_detection,hint_for_detection,
            get_root_production,
            mention_level,
            svm_EMP_ORG_Employ_Undetermined_reverse]
            #svm_PHYS_Part_Whole,
            #svm_EMP_ORG_Subsidiary,svm_EMP_ORG_Subsidiary_reverse,
            #svm_PER_SOC_Family,svm_PER_SOC_Business]

def dumn(coref,corpus):
    return True

def tree_height(coref,corpus):
    pt = coref.pt_tree
    curr_node = pt.index[0]
    while curr_node.parent() != None:
        curr_node = curr_node.parent()
    return curr_node.height()

def distance_n(coref,n):
    """number of word between two mentions"""
    diff = coref.second.start-coref.first.end
    return diff<=n

def dist_seg(coref,corpus):
    if dist_0(coref,corpus): return '0'
    if dist_1(coref,corpus): return '1'
    if dist_4(coref,corpus): return '2'
    if dist_6(coref,corpus): return '3'
    return '4'

def dist_0(coref,corpus):
    return distance_n(coref,0)
def dist_1(coref,corpus):
    return distance_n(coref,1)
def dist_4(coref,corpus):
    return distance_n(coref,4)
def dist_6(coref,corpus):
    return distance_n(coref,6)

def head_word(document,mention,corpus):
    list=corpus.postagged_data[document][mention.sent].tokens[mention.start:mention.end]
    hasprp= map(lambda x:x[1]=='IN',list)

    if True in hasprp:
        return list[hasprp.index(True) -1][0]
    else:
        return list[-1][0]

def head_word_m1(coref,corpus):
    return head_word(coref.document,coref.first,corpus)

def head_word_m2(coref,corpus):
    return head_word(coref.document,coref.second,corpus)


def entity_type(coref,corpus):
    return coref.first.ne+'-'+coref.second.ne

def mention_level(coref,corpus):
    document = coref.document
    first = coref.first
    second = coref.second
    Postag_first = corpus.postagged_data[document][first.sent].tokens[first.start:first.end]
    Postag_second = corpus.postagged_data[document][second.sent].tokens[second.start:second.end]
    return get_mention_level(Postag_first[-1][1]) + '-' + get_mention_level(Postag_second[-1][1])

def get_mention_level(pos):
    if (pos == 'NN' or pos == 'NNS'): return '0'
    if (pos == 'NNP' or pos == 'NNPS'): return '1'
    if ('PRP' in pos): return '2'
    return '3'

def svm_PHYS_Part_Whole(coref,corpus):
    return coref.svm_result[0]

def svm_EMP_ORG_Employ_Undetermined_reverse(coref,corpus):
    return coref.svm_result[1]

def svm_EMP_ORG_Subsidiary(coref,corpus):
    return coref.svm_result[2]

def svm_EMP_ORG_Subsidiary_reverse(coref,corpus):
    return coref.svm_result[3]

def svm_PER_SOC_Family(coref,corpus):
    return coref.svm_result[4]

def svm_PER_SOC_Business(coref,corpus):
    return coref.svm_result[5]


def get_root_production(coref,corpus):
    pt = coref.pt_tree
    curr_node = pt.index[0]
    while curr_node.parent() != None:
        curr_node = curr_node.parent()
    return curr_node[0].label()+'-'+curr_node[-1].label() 

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


def chunk_between(coref,corpus):
    chunkline=corpus.chunk_data[coref.document][coref.first.sent]
    posline=corpus.sentence_data[coref.document][coref.first.sent]
    chunks=chunkline.chunks_between(posline.postag_index[coref.first.end],posline.postag_index[coref.second.start])
    return chunkline,chunks

def chunk_before(coref,corpus):
    chunkline=corpus.chunk_data[coref.document][coref.first.sent]
    posline=corpus.sentence_data[coref.document][coref.first.sent]
    chunks=chunkline.chunks_before(posline.postag_index[coref.first.start])
    return chunkline,chunks

def chunk_after(coref,corpus):
    chunkline=corpus.chunk_data[coref.document][coref.first.sent]
    posline=corpus.sentence_data[coref.document][coref.first.sent]
    chunks=chunkline.chunks_after(posline.postag_index[coref.second.start])
    return chunkline,chunks

def chunk_hbnull(coref,corpus):
    chunkline,chunks=chunk_between(coref,corpus)
    return len(chunks) > 0

def chunk_hbfl(coref,corpus):
    chunkline,chunks=chunk_between(coref,corpus)
    print chunks
    return chunkline.words[chunks[0][0]].heads if len(chunks) ==1 else 'None'

def chunk_hbf(coref,corpus):
    chunkline,chunks=chunk_between(coref,corpus)
    print chunks
    return chunkline.words[chunks[0][0]].heads if len(chunks) >1 else 'None'

def chunk_hbl(coref,corpus):
    chunkline,chunks=chunk_between(coref,corpus)
    print chunks
    return chunkline.words[chunks[-1][0]].heads if len(chunks) >1 else 'None'


def chunk_m1f(coref,corpus):
    chunkline,chunks=chunk_before(coref,corpus)
    print chunks
    return chunkline.words[chunks[-1][0]].heads if len(chunks) >0 else 'None'

def chunk_m2l(coref,corpus):
    chunkline,chunks=chunk_before(coref,corpus)
    print chunks
    return chunkline.words[chunks[-2][0]].heads if len(chunks) >1 else 'None'



def chunk_m2f(coref,corpus):
    chunkline,chunks=chunk_after(coref,corpus)
    print chunks
    return chunkline.words[chunks[0][0]].heads if len(chunks) >0 else 'None'

def chunk_m2l(coref,corpus):
    chunkline,chunks=chunk_after(coref,corpus)
    print chunks
    return chunkline.words[chunks[1][0]].heads if len(chunks) >1 else 'None'


if __name__ == '__main__':
    from data_reader import *
    from feature_extraction import FeatureExtraction
    from build_corpus import BuildCorpus
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.test(DataSet(r"./project3/data/rel-trainset.gold"),chunk_hbfl)
