def maxent2weka(in_file='rel-maxent.train',out_file='rel-train.arff'):
    classes = set()
    feature = []
    feat_dict = dict()
    f_o = open(out_file,'w')
    output_buffer = '\n@DATA\n'
    with open(in_file,'r') as f_i:
        line = f_i.readline()[:-1].split(' ')
        classes.add(line[0])
        value_list = []
        for pair in line[1:]:
            feat,value = get_feat_value(pair)
            feature.append(feat)
            value_list.append(value)
            feat_dict[feat] = set([value])
        output_buffer += ','.join(value_list) + ','+line[0]+'\n'

        for line in f_i:
            splitted = line[:-1].split(' ')
            classes.add(splitted[0])
            value_list = add_to_dict(splitted[1:],feat_dict)
            output_buffer += ','.join(value_list) + ','+splitted[0]+'\n'
    f_o.write('@RELATION '+ in_file[-4:]+'\n\n')
    for feat in feature:
        f_o.write('@ATTRIBUTE '+feat+' '+'{'+','.join(feat_dict[feat])+'}'+'\n')
    f_o.write('@ATTRIBUTE class '+'{'+','.join(classes)+'}'+'\n')
    f_o.write(output_buffer)
    f_o.close()
        
def add_to_dict(pair_list,feat_dict):
    value_list = []
    for pair in pair_list:
        feat,value = get_feat_value(pair)
        feat_dict[feat].add(value)
        value_list.append(value)
    return value_list
def get_feat_value(string):
    splitted = string.split('=')
    return splitted[0],splitted[1]

if __name__ == '__main__':
    maxent2weka()
