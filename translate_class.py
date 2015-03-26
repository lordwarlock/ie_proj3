import re
def translate_class(in_file = './project3/data/svm-light-files/rel-train-parsed-data',
                    out_file = './project3/data/svm-ova-light-files/rel-train-parsed-data'):
    f_out = open(out_file,'w')
    f_in = open(in_file,'r')
    counter = 0
    for line in f_in:
        match = re.match('(.*? )(\|BT\|.*)',line)
        #if match and match.group(1).strip() == 'PHYS.Located':
        #PER-SOC 88/50 EMP-ORG 81/50
        if match and 'EMP-ORG.Employ-Staff.reverse' in match.group(1).strip():
            f_out.write('1' + ' ' + match.group(2)+'\n')
        else:
            f_out.write('-1' + ' ' + match.group(2)+'\n')
        counter += 1
    f_in.close()

if __name__ == '__main__':
    for data in ['train','dev','test']:
        translate_class('./project3/data/svm-light-files/rel-{}-parsed-data'.format(data),'./project3/data/svm-ova-light-files/rel-{}-parsed-data'.format(data))
