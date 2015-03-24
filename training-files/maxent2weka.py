def maxent2weka(in_file='rel-maxent.train',
                out_file='rel-train.arff',
                test_file='rel-maxent.test',
                test_out_file='rel-test.arff'):
    classes = set()
    feature = []
    feat_dict = dict()
    f_o = open(out_file,'w')
    f_o_test = open(test_out_file,'w')
    """output_buffer = '\n@DATA\n'
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
            output_buffer += ','.join(value_list) + ','+splitted[0]+'\n'"""
    output_test = get_data_text(test_file,test_out_file,classes,feat_dict,[])
    output_train = get_data_text(in_file,out_file,classes,feat_dict,feature)
    header = get_header_text(feature,feat_dict,classes)
    f_o.write('@RELATION '+ in_file[-4:]+'\n\n')
    f_o.write(header)
    f_o.write(output_train)
    f_o.close()

    f_o_test.write('@RELATION '+ test_file[-4:]+'\n\n')
    f_o_test.write(header)
    f_o_test.write(output_test)
    f_o_test.close()
    """header_buffer = ''
    f_o.write('@RELATION '+ in_file[-4:]+'\n\n')
    for feat in feature:
        f_o.write('@ATTRIBUTE '+feat+' '+'{'+','.join(feat_dict[feat])+'}'+'\n')
    f_o.write('@ATTRIBUTE class '+'{'+','.join(classes)+'}'+'\n')
    f_o.write(output_buffer)
    f_o.close()"""

def get_header_text(feature,feat_dict,classes):
    header_buffer = ''
    #header_buffer += '@RELATION '+ in_file[-4:]+'\n\n'
    for feat in feature:
        header_buffer += '@ATTRIBUTE '+feat+' '+'{'+','.join(feat_dict[feat])+'}'+'\n'
    header_buffer += '@ATTRIBUTE class '+'{'+','.join(classes)+'}'+'\n'
    return header_buffer

def get_data_text(in_file,out_file,classes,feat_dict,feature):
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
    return output_buffer
        
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
