

class OutputGenerator(object):
    """description of class"""

    def __init__(self,corpus):
        self.corpus=corpus

    def output(dataset,input,output):
         with open(input,'r') as fi:
            with open(output,'w') as fo:
                for line,relation in zip(fi,dataset.data):

