from nltk import ParentedTree
from collections import Counter
from build_corpus import BuildCorpus

class DataSet(object):
    """description of class"""
    def __init__(self,file='./project3/data/rel-trainset.gold',haslabel=True):
        self.haslabel=haslabel
        self.dict={}
        self.data=[]
        with open(file) as f:
            for line in f:
                values=line.split()
                if haslabel:
                    docname=values[1]
                else:
                    docname=values[0]
                list=self.dict.get(docname,[])
                coref=Coref(values,haslabel)
                list.append(coref)
                self.data.append(coref)



class Coref(object):
    def __init__(self,list,haslabel):
        
        if haslabel:
            self.label = list[0]
            list=list[1:]
        else:
            self.label=None
        self.document=list[0]
        self.first = Markable()
        self.second = Markable()
        self.first.sent, self.first.start, self.first.end, self.first.ne, _, self.first.word = list[1:7]
        self.second.sent, self.second.start, self.second.end, self.second.ne, _, self.second.word = list[7:]
        self.first.start = int(self.first.start)
        self.second.start = int(self.second.start)
        self.first.end = int(self.first.end)
        self.second.end = int(self.second.end)
        self.first.sent = int(self.first.sent)
        self.second.sent = int(self.second.sent)

class Markable(object):
    pass


class Document(object):

    def __init__(self,fparsed,fpos):
        self.sents=[]
        self.trees=[]
        with open(fparsed,'r') as f1:
            with open(fpos,'r') as f2:
                poslines=filter(lambda x:x.strip() != '', f2.readlines())
                lines=f1.readlines()
                for line,pos in zip(lines,poslines):
                    tree=ParentedTree.fromstring(line,read_leaf=read_node)
                    self.sents.append(tree)

class Corpus(object):
    def __init__(self,folder):
        pass

class DataAnalysis():
    def __init__(self,data_file='./project3/data/rel-trainset.gold'):
        self.data = DataSet(data_file).data
        self.pn = self.positive_number()
        self.classes = self.classes_info()
        self.corpus = BuildCorpus()
    def positive_number(self):
        pn = 0
        for d in self.data:
            if (d.label != 'no_rel'):
                pn += 1
        return pn

    def classes_info(self):
        classes_dict = Counter()
        for d in self.data:
            if (d.label != 'no_rel'):
                classes_dict[d.label] += 1
        sum_pos = sum(classes_dict.values())
        for key,value in classes_dict.items():
            classes_dict[key] = ( value + 0.0) / sum_pos
        return classes_dict

    def mention_distance(self):
        data_counter = 0
        distance_dict = Counter()
        for d in self.data:
            data_counter+=1
            if (d.label != 'no_rel'):
                distance = - d.first.end + d.second.start
                if (d.first.end > d.second.start):
                    print d.first.sent==d.second.sent,data_counter
                distance_dict[distance] += 1
        return distance_dict

    def link_word(self):
        link_dict = dict()
        for key in self.classes.keys():
            link_dict[key] = Counter()
        for d in self.data:
            if(d.label != 'no_rel'):
                doc = d.document
                start = d.first.end
                end = d.second.start
                sentence = self.corpus.postagged_data[doc][d.first.sent]
                if start == end:
                    link_dict[d.label]['--None--'] += 1
                for token in sentence.tokens[start:end]:
                    link_dict[d.label][token[0].lower()] += 1
        return link_dict

if __name__ == '__main__':

    da = DataAnalysis('./project3/data/rel-testset.gold')
    ld = da.link_word()
    for key in ld.keys():
        print key,'--------------------------------------'
        for token,value in ld[key].items():
            print token,value
