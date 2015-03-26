import re
from subprocess import call

def translate_class(in_file = './project3/data/svm-light-files/rel-train-parsed-data',
                    out_file = './project3/data/svm-ova-light-files/rel-train-parsed-data',
                    tag = 'EMP-ORG.Employ-Staff.reverse'):
    f_out = open(out_file,'w')
    f_in = open(in_file,'r')
    counter = 0
    for line in f_in:
        match = re.match('(.*? )(\|BT\|.*)',line)
        #if match and match.group(1).strip() == 'PHYS.Located':
        #PER-SOC 88/50 EMP-ORG 81/50
        if match and tag in match.group(1).strip():
            f_out.write('1' + ' ' + match.group(2)+'\n')
        else:
            f_out.write('-1' + ' ' + match.group(2)+'\n')
        counter += 1

        #if (counter == 600): break

    f_out.close()
    f_in.close()

if __name__ == '__main__':
    with open('./stats/train_classes','r') as f_c:
        for line in f_c:
            splitted = line.split()
            tag = splitted[0]
            print tag
            o_file = '/Users/zheng/documents/ie/ie_proj3/project3/data/svm-ova-light-files/results-t/log-{}'.format(tag)
            f_o = open(o_file,'w')
            for data in ['train','dev','test']:
                translate_class('./project3/data/svm-light-files/rel-{}-parsed-data'.format(data),'./project3/data/svm-ova-light-files/rel-{}-parsed-data'.format(data),tag)
            call(['/Users/zheng/documents/tools/svm-light-TK-1.2/svm-light-TK-1.2.1/svm_learn',
                  '-t','5',
                  '/Users/zheng/documents/ie/ie_proj3/project3/data/svm-ova-light-files/rel-train-parsed-data',
                  '/Users/zheng/documents/ie/ie_proj3/project3/data/svm-ova-light-files/train_model'])

            call(['/Users/zheng/documents/tools/svm-light-TK-1.2/svm-light-TK-1.2.1/svm_classify',
                  '/Users/zheng/documents/ie/ie_proj3/project3/data/svm-ova-light-files/rel-train-parsed-data',
                  '/Users/zheng/documents/ie/ie_proj3/project3/data/svm-ova-light-files/train_model',
                  '/Users/zheng/documents/ie/ie_proj3/project3/data/svm-ova-light-files/results-t/{}'.format(tag)],
                  stdout=f_o)
