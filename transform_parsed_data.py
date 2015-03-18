import glob
import re

def transform(dir_name = './project3/data/postagged-files/*.tag'):
    files = glob.glob(dir_name)
    for file in files:
        new_file = re.sub('postagged-files','t-postagged-files',file)
        print new_file
        f_out = open(new_file,'w')
        with open(file,'r') as f_in:
            for line in f_in:
                new_line = re.sub('\(','[',line)
                new_line = re.sub('\)',']',new_line)
                f_out.write(new_line)
        f_out.close()

if __name__ == '__main__':
    transform()
