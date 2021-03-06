import glob
import re
from nltk.tree import ParentedTree

class SentLine(object):
    """Parsed sentence"""
    def __init__(self,line):
        self.raw = line
        self.true_index = None
        self.index=[]
        def read_leaf(str):
            leaf_node=ParentedTree(str,[])
            self.index.append(leaf_node)
            return leaf_node
        self.tree = ParentedTree.fromstring(line,read_leaf=read_leaf)

class ChunkWord(object):
    """Chunk word"""
    def __init__(self,line):
        self.doc,self.sent_id,self.word_id,self.iob_inner,self.word,self.heads,self.head_ids,self.iob_chain=line.split()
        self.sent_id=int(self.sent_id)
        self.word_id=int(self.word_id)


class ChunkSent(object):
    def __init__(self,words):
        self.chunks=[]
        self.chunk_mapping=[]
        self.words=words
        chunk=-1
        for i,word in enumerate(words):
            if word.iob_inner.startswith('B'):
                chunk+=1
                self.chunk_mapping.append(chunk)
                start = i
            elif word.iob_inner.startswith('E'):
                self.chunk_mapping.append(chunk)
                self.chunks.append((start,i+1))
            elif word.iob_inner.startswith('C'):
                chunk+=1
                self.chunk_mapping.append(chunk)
                self.chunks.append((i,i+1))
            elif word.iob_inner.startswith('I'):
                self.chunk_mapping.append(chunk)
            else:
                self.chunk_mapping.append(-1)
    
    def chunks_between(self,first,second):
        if self.chunk_mapping[first] != -1:
            first=self.chunk_mapping[first] + 1
        else:
            while self.chunk_mapping[first] == -1:
                first += 1
                if first >= len(self.chunk_mapping): return []
            first=self.chunk_mapping[first]

        if self.chunk_mapping[second] != -1:
            second=self.chunk_mapping[second] - 1
        else:
            while self.chunk_mapping[second] == -1:
                second -= 1
                if second <0: return []
            second=self.chunk_mapping[second]

        return self.chunks[first:second+1]

    def chunks_before(self,index):
        if self.chunk_mapping[index] != -1:
            index=self.chunk_mapping[index] -1
        else:
            while self.chunk_mapping[index] == -1:
                index -= 1
                if index <0: return []
            index=self.chunk_mapping[index]
        return self.chunks[:index+1]

    def chunks_after(self,index):
        if self.chunk_mapping[index] != -1:
            index=self.chunk_mapping[index] +1
        else:
            while self.chunk_mapping[index] == -1:
                index += 1
                if index >= len(self.chunk_mapping): return []
            index=self.chunk_mapping[index]

        return self.chunks[index:]

class PosLine(object):
    """store tokens with pos tag"""
    def __init__(self,line):
        token_poses = line.split()
        self.tokens = []
        for token_pos in token_poses:
            match = re.match('(.*)_(.*)',token_pos)
            self.tokens.append((match.group(1),match.group(2)))

    def __str__(self):
        return str(self.tokens)

class BuildCorpus(object):
    """build the corpus for all data"""
    def __init__(self):
        self.postagged_data = dict()
        self.sentence_data = dict()
        self.chunk_data = dict()
        self.corpus = None
        self.build_chunk_data()
        self.build_postagged_data()
        self.build_sentence_data()
        self.fix_indexes()

    def build_postagged_data(self,directory='./project3/data/t-postagged-files'):
        """store postagged data into a dictionary where the key is document name"""
        pos_files = glob.glob(directory+'/*.tag')
        regex=re.compile(r'.*[/|\\](.*?)\.head\.rel\.tokenized\.raw\.tag')
        for pos_file in pos_files:
            with open(pos_file,'r') as f_pos:
                match = regex.match(pos_file)
                data_name = match.group(1)
                lines = []
                for line in f_pos:
                    if (line == '\n'): continue
                    lines.append(PosLine(line))
                self.postagged_data[data_name] = lines

    def build_sentence_data(self,directory='./project3/data/t-parsed-files'):
        """store parsed sentence into a dictionary where the key is document name"""
        sentence_files = glob.glob(directory+'/*.parse')
        for sentence_file in sentence_files:
            with open(sentence_file,'r') as f_sent:
                match = re.match(r'.*[/|\\](.*?)\.head\.rel\.tokenized\.raw\.parse',sentence_file)
                data_name = match.group(1)
                lines = []
                for line in f_sent:
                    if line == '\n':continue
                    lines.append(SentLine(line))
                self.sentence_data[data_name] = lines

    def build_chunk_data(self,directory='./chunking'):
        """store parsed sentence into a dictionary where the key is document name"""
        sentence_files = glob.glob(directory+'/*.chunk')
        for sentence_file in sentence_files:
            with open(sentence_file,'r') as f_sent:
                match = re.match(r'.*[/|\\](.*?)\.head\.rel\.tokenized\.raw\.chunk',sentence_file)
                data_name = match.group(1)
                lines = []
                words = []
                sentid = 1
                for line in f_sent:
                    if line == '\n' or line.startswith('#'):continue
                    word=ChunkWord(line)
                    if word.sent_id != sentid:
                        sent=ChunkSent(words)
                        lines.append(sent)
                        words=[]
                    sentid=word.sent_id
                    words.append(word)

                sent=ChunkSent(words)
                lines.append(sent)
                self.chunk_data[data_name] = lines


    def fix_indexes(self):
        """Due to the disagreement of tokenization between postagged and parsed files
           this function will add a mapping list, to map index in parsed file to 
           postagged file"""
        for doc_name in self.postagged_data.iterkeys():
            pos_lines = self.postagged_data[doc_name]
            sen_lines = self.sentence_data[doc_name]
            for line_index in range(len(pos_lines)):
                true_index = [0 for i in range(len(sen_lines[line_index].index))]
                sent_index = 0
                for token_index in range(len(pos_lines[line_index].tokens)):
                    remain =  pos_lines[line_index].tokens[token_index][0]
                    while(1):
                        if (sent_index == len(sen_lines[line_index].index)):break
                        sen_token = sen_lines[line_index].index[sent_index].label()
                        if (sen_token == "n't"):
                            sen_token = sen_token[-len(remain):]
                        if (len(sen_token) > len(remain)):
                            break
                        if (sen_token == remain[:len(sen_token)]):
                            true_index[sent_index] = token_index
                            sent_index += 1
                            remain = remain[len(sen_token):]
                        else:
                            break
                postag_index=list(range(len(pos_lines[line_index].tokens)))
                start = 0
                add = 0
                for i,j in enumerate(true_index):
                    postag_index[j] = max(postag_index[j],i)
                sen_lines[line_index].true_index = true_index
                sen_lines[line_index].postag_index = postag_index

    def prune_trees(self,dataset,input,output):
        with open(input,'r') as fi:
          with open(output,'w') as fo:
            for line,relation in zip(fi,dataset.data):
                if relation.first.sent != relation.second.sent:
                    continue
                sent = self.sentence_data[relation.document][relation.first.sent]
                sent1 = SentLine(line)
                leftindex=relation.first.start
                rightindex=relation.second.end - 1
                left = sent1.index[sent.postag_index[leftindex]]
                right = sent1.index[sent.postag_index[rightindex]]
                self.tree_crop_merge(left)
                tree = self.tree_crop_merge(right,1)
                while len(tree) == 1:
                    tree = tree[0]
                fo.write(re.subn(r'\s+',' ',re.subn(r'\(([^()]+?)\s*\)','\\1',str(tree))[0])[0] + '\n')

    def tree_crop_merge(self,tree,dir=0):
        parent = tree.parent()
        child = tree
        while parent != None:
            index = child.parent_index()
            if dir==0:
                del parent[:index]
            else:
                del parent[index+1:]
            if child.label() == parent.label() and len(parent) ==1:
                subtree=parent.pop()
                if parent.parent() == None:
                    return subtree
                else:
                    parent.parent()[parent.parent_index()]=subtree
                    parent=subtree

            child=parent
            parent=parent.parent()
        return child
            



if __name__ == '__main__':
    bc = BuildCorpus()
    from data_reader import DataSet
    from output_generate import OutputGenerator
    for data in ['train','dev','test']:
        ds = DataSet('project3/data/rel-{}set.gold'.format(data))
        pt = bc.prune_trees(ds,r'project3/data/e-parsed-files/rel-{}-parsed-data'.format(data),r'project3/data/p-parsed-files/rel-{}-parsed-data'.format(data))
        OutputGenerator(bc).output(ds,r'project3/data/p-parsed-files/rel-{}-parsed-data'.format(data),r'project3/data/svm-light-files/rel-{}-parsed-data'.format(data))
    """p = bc.postagged_data['APW20001001.2021.0521']
    t = bc.sentence_data['APW20001001.2021.0521']
    print t[3].true_index
    true_index = [0 for i in range(len(t[3].index))]
    t_index = 0
    print 'start'
    for i in range(len(p[3].tokens)):
        print p[3].tokens[i]
        while(1):
            if (t_index == len(t[3].index)):break
            print t_index,t[3].index[t_index].label(),p[3].tokens[i][0]
            if (t[3].index[t_index].label() in p[3].tokens[i][0]):
                true_index[t_index] = i
                t_index += 1
            else:
                break

    print true_index"""
