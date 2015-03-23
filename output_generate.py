

class OutputGenerator(object):
    """description of class"""

    def __init__(self,corpus):
        self.corpus=corpus

    def output(self,dataset,tree,output):
         with open(tree,'r') as fi:
            with open(output,'w') as fo:
                for line,relation in zip(fi,dataset.data):
                    fo.write('{} |BT| {} |ET|\n'.format(relation.label,line.strip()))
