from feature_functions import get_feature_functions
from data_reader import *
from build_corpus import BuildCorpus


class FeatureExtraction(object):
    """Extract Features"""
    def __init__(self,corpus=None):
        self.corpus = corpus
        self.feat = []
        self.data= None
        self.weka_attr = []

    def test(self,dataset,feature):
        """Just for testing"""
        ffunc_list = get_feature_functions()
        for index,line in enumerate(dataset.data):
            print line.label,line.first.word,line.first.ne,line.second.word,line.second.ne,feature(line,self.corpus)

    def extract(self,dataset):
        """Extract features using corresponding feature functions"""
        ffunc_list = get_feature_functions()
        for index,line in enumerate(dataset.data):
            if line==None:
                self.feat.append(None)
            else:
                featuredict={ffunc.__name__:str(ffunc(line,self.corpus)) for ffunc in ffunc_list}
                if dataset.haslabel:
                    featuredict['label']=line.label
                self.feat.append(featuredict)

    def mallet_output(self,line):
        """output in maxent format"""
        label=None
        list=[]
        for key,value in line.iteritems():
            if key=='label':
                label=value
                continue
            list.append(key + '=' + str(value))
        return ('' if label==None else label + ' ') +  ' '.join(list)

    def output_feat(self,filename,linefunc):
        with open(filename,'w') as output_file:
            for line in self.feat:
                
                output_file.write(linefunc(line) + '\n')

    def weka_output(self,line):
        """output in weka format, but without the header"""
        label = None
        result = ''
        for key,value in line.iteritems():
            if key == 'label':
                label = value
                continue
            if key not in self.weka_attr: self.weka_attr.append(key)
            result += str(value) + ', '
        return result + label
"""
@RELATION coref_test

@ATTRIBUTE distance	numeric
@ATTRIBUTE gender_agree	{True,False,None}
@ATTRIBUTE both_pronoun	{0,1,2}
@ATTRIBUTE demonstrative	{True,False}
@ATTRIBUTE definite	{True,False}
@ATTRIBUTE sub_str	{True,False}
@ATTRIBUTE ne_match	{True,False}
@ATTRIBUTE appositive	{True,False}
@ATTRIBUTE alias	{True,False}
@ATTRIBUTE str_match	{True,False}
@ATTRIBUTE hint_who_detection	{True,False}
@ATTRIBUTE pronoun_2_v01	{True,None}
@ATTRIBUTE number_agree	{True,False,None}
@ATTRIBUTE capital_i_j	{0,1,2}
@ATTRIBUTE hint_word_detection	{True,False}
@ATTRIBUTE prp_str_match	{True,False}
@ATTRIBUTE pronoun_1_v01	{True,None}
@ATTRIBUTE prp_str_match_v01	{True,False}
@ATTRIBUTE class 	{yes, no}

@DATA
"""
if __name__=='__main__':
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.extract(DataSet(r"./project3/data/rel-trainset.gold"))
    f_ex.output_feat(r"weka-trainset.arff",f_ex.weka_output)
    print f_ex.weka_attr
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.extract(DataSet(r"./project3/data/rel-testset.gold"))
    f_ex.output_feat(r"weka-testset.arff",f_ex.weka_output)
