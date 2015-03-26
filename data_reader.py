from nltk import ParentedTree
from collections import Counter
from build_corpus import BuildCorpus
from build_corpus import SentLine
import re

class DataSet(object):
    """description of class"""
    def __init__(self,file='./project3/data/rel-trainset.gold',
                      pt_file = './project3/data/svm-light-files/rel-train-parsed-data',
                      svm_file = './project3/data/svm-ova-light-files/results-t/',
                      haslabel=True):
        self.haslabel=haslabel
        self.dict={}
        self.data=[]
        f_pt = open(pt_file,'r')
        svm_result = self.get_svm_results(svm_file)
        counter = 0
        with open(file) as f:
            for line in f:
                counter+=1
                values=line.split()
                if haslabel:
                    docname=values[1]
                else:
                    docname=values[0]
                list=self.dict.get(docname,[])
                pt_line = re.search('\|BT\|(.*?)\|ET\|',f_pt.readline()).group(1)
                try:
                    pt_tree = SentLine(pt_line)
                except:
                    print counter,pt_line
                coref=Coref(values,haslabel,pt_tree,svm_result[counter-1])
                list.append(coref)
                self.data.append(coref)

    def get_svm_results(self,svm_file):
        class_list = []
        result = dict()
        with open('./stats/svm-tree-useful-classes') as f_c:
            for line in f_c:
                class_list.append(line[:-1])

        for rel_class in class_list:
            counter = 0
            with open(svm_file+rel_class,'r') as f_s:
                for line in f_s:
                    if counter in result:
                        result[counter].append(float(line)>0)
                    else:
                        result[counter] = [float(line)>0]
                    counter += 1
        return result


class Coref(object):
    def __init__(self,list,haslabel,pt_tree=None,svm_result=None):
        
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
        self.pt_tree = pt_tree
        self.svm_result = svm_result
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

    def root_production(self):
        production_dict = dict()
        for key in self.classes.keys():
            production_dict[key] = Counter()
        for d in self.data:
            if d.label == 'no_rel': continue
            production_dict[d.label][self.get_root_production(d)] += 1
        return production_dict

    def get_root_production(self,data):
        pt = data.pt_tree
        curr_node = pt.index[0]
        while curr_node.parent() != None:
            curr_node = curr_node.parent()
        return curr_node[0].label()+'-'+curr_node[-1].label() 
if __name__ == '__main__':

    da = DataAnalysis('./project3/data/rel-testset.gold')
    result = da.root_production()
    for key in result.keys():
        print key,'--------------------------------------'
        sorted_result = sorted(result[key].items(),key=lambda x:x[1],reverse = True)
        for prod,value in sorted_result:
            print prod,value
    """for key in ld.keys():
        print key,'--------------------------------------'
        for token,value in ld[key].items():
            print token,value"""
