def evaluate(in_file):
    with open(in_file,'r') as f_i:
        _ = f_i.readline()
        gold = []
        pred = []
        for line in f_i:
            if line == '\n': continue
            splitted = line.split()
            #print splitted[1].split(':')
            gold.append(splitted[1].split(':')[1])
            pred.append(splitted[2].split(':')[1])

    test_total = 0
    gold_total = 0
    correct = 0

    #print gold_tag_list
    #print test_tag_list

    for i in range(len(gold)):
        if gold[i] != 'no_rel':
            gold_total += 1
        if pred[i] != 'no_rel':
            test_total += 1
        if gold[i] != 'no_rel' and gold[i] == pred[i]:
            correct += 1


    precision = float(correct) / test_total
    recall = float(correct) / gold_total
    f = precision * recall * 2 / (precision + recall)

    #print correct, gold_total, test_total
    print 'precision =', precision, 'recall =', recall, 'f1 =', f

if __name__ == '__main__':
    evaluate('prediction')
