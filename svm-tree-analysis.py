import glob
import re
class SVMTreeAnalysis():
    def __init__(self,results_dir = './project3/data/svm-ova-light-files/results/log*'):
        self.results_dir = results_dir

    def read_files(self):
        result = dict()
        files_list = glob.glob(self.results_dir)
        for file_dir in files_list:
            class_name,precision,recall = self.get_precision_recall(file_dir)
            result[class_name] = (precision,recall)
        print result
    def get_precision_recall(self,file_dir):
        class_match = re.match('.*/log-(.*)',file_dir)
        if class_match: class_name = class_match.group(1)
        with open(file_dir,'r') as f_i:
            for line in f_i:
                match = re.match('Precision/recall on test set: (.*?)%/(.*)%\n',line)
                if match:
                    try:
                        precision = float(match.group(1))
                    except:
                        precision = 0.0
                    try:
                        recall = float(match.group(2))
                    except:
                        recall = 0.0
        return class_name,precision,recall

if __name__ == '__main__':
    sta = SVMTreeAnalysis()
    sta.read_files()
