from data_reader import DataSet
from build_corpus import BuildCorpus
from build_corpus import SentLine
from nltk.tree import ParentedTree
from nltk.tree import Tree
import copy

class AddEntityToTree(object):
    def __init__(self,data=DataSet(file='./project3/data/rel-devset.gold').data,
                      corpus=BuildCorpus(),
                 output='./project3/data/e-parsed-files/rel-dev-parsed-data'):
        self.data = data
        self.corpus = corpus
        self.output = output
        self.process_each_mention()

    def process_each_mention(self):
        """add entity type as the parent of the entity leaf"""
        with open(self.output,'w') as f_out:
            counter = 1
            for coref in self.data:
                doc = coref.document
                print doc,counter
                counter += 1
                sentence = self.corpus.sentence_data[doc][coref.first.sent]
                true_index = copy.deepcopy(sentence.true_index)
                sentence = SentLine(sentence.raw)
                sentence.true_index = true_index
                self.add_entity_type_to_tree(sentence,
                                             coref.first.ne,
                                             coref.first.start,
                                             coref.first.end)

                self.add_entity_type_to_tree(sentence,
                                             coref.second.ne,
                                             coref.second.start,
                                             coref.second.end)
                f_out.write(sentence.tree.pprint(margin=8096)+'\n')

    def add_entity_type_to_tree(self,sentence,ne,start,end):
        entity_nodes = self.get_nodes_list_by_index(sentence,start,end)
        if (len(entity_nodes) > 1):
            insertion_node = self.get_lowest_common_ancestor(entity_nodes)
            insertion_parent = insertion_node.parent()
            insertion_index = insertion_parent.index(insertion_node)
            insertion_parent.remove(insertion_node)
            new_node = ParentedTree(insertion_node.label(),[insertion_node])
            insertion_node.set_label(ne)
            insertion_parent.insert(insertion_index,new_node)
        else:
            parent = entity_nodes[0].parent()
            pos_tag = parent.label()
            parent.set_label(ne)
            parent.pop()
            parent.append(ParentedTree(pos_tag,[entity_nodes[0]]))

    def get_nodes_list_by_index(self,sentence,start,end):
        nodes_list = []
        for sent_index in range(len(sentence.index)):
            if ((sentence.true_index[sent_index] >= start)\
                and\
                (sentence.true_index[sent_index] < end)):
                nodes_list.append(sentence.index[sent_index])
        if (nodes_list == []):
            print sentence.tree
            print start,end,sentence.true_index
        return nodes_list

    def get_lowest_common_ancestor(self,leaf_list):
        """get the lowest common ancestor of leaves in the list"""
        if (len(leaf_list) == 1):
            return leaf_list
        first_node = leaf_list[0]
        #the first parent is the pos tag of the leaf
        #we should not insert here
        curr_node = first_node.parent().parent()
        for leaf in leaf_list[1:]:
            first_ancestor_list = [curr_node]

            while curr_node != None:
                first_ancestor_list.append(curr_node)
                curr_node = curr_node.parent()
            curr_node = leaf.parent()

            flag = False
            while curr_node != None:
                if (curr_node in first_ancestor_list):
                    flag = True
                    break
                curr_node = curr_node.parent()
            if (flag):continue
            else: return False

        return curr_node

if __name__ == '__main__':
    att = AddEntityToTree()
