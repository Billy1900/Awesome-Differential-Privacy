import pandas
import os
import random

ATTNAME = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital-status',
           'occupation', 'relationship', 'race', 'sex',
           'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'class']

AGECONFFILE = '../conf/age_hierarchy.txt'
EDUCONFFILE = '../conf/edu_hierarchy.txt'
MARITALCONFFILE = '../conf/marital_hierarchy.txt'
RACECONFFILE = '../conf/race_hierarchy.txt'


def readdata(filepath='../data', filename='adult.data'):
    records = []
    try:
        with open(os.path.join(filepath, filename), 'r') as rf:
            for line in rf:
                line = line.strip()
                if not line:
                    continue
                line = [a.strip() for a in line.split(',')]
                # print(line)
                intidx = [ATTNAME.index(colname) for colname in (
                    'age', 'fnlwgt', 'education_num', 'capital-gain', 'capital-loss', 'hours-per-week')]
                for idx in intidx:
                    try:
                        line[idx] = int(line[idx])
                    except:
                        print('attribute %s, value %s, cannot be converted to number' % (ATTNAME[idx], line[idx]))
                        line[idx] = -1
                for idx in range(len(line)):
                    if line[idx] == '' or line[idx] == '?':
                        line[idx] = '*'
                records.append(line)
        return records
    except:
        print('cannot open file: %s:%s' % (filepath, filename))


def generate_data_for_laplace_mechanism(records):
    """
    generate the three different versions datasets for Laplace Mechanism
    
    Arguments:
            records {[list of list]} -- [original records for adult datasets]
    
    Returns:
            three versions datasets for Laplace Mechanism
            oldest age and youngest age
    """

    oldestidx, twentysixidx, youngestidx = -1, -1, -1
    oldest, youngest = -float('inf'), float('inf')
    ageidx = ATTNAME.index('age')
    for idx, record in enumerate(records):
        """
        age == -1 means the value is missing in the dataset
        """
        if record[ageidx] == -1:
            continue
        if record[ageidx] >= oldest:
            if record[ageidx] != oldest or random.random() >= 0.5:
                oldestidx, oldest = idx, record[ageidx]
        if record[ageidx] <= youngest:
            if record[ageidx] != youngest or random.random() >= 0.5:
                youngestidx, youngest = idx, record[ageidx]
        if record[ageidx] == 26 and (twentysixidx != -1 or random.random() >= 0.5):
            twentysixidx = idx
    version1 = _copy_with_exclude_idx(records, oldestidx)
    version2 = _copy_with_exclude_idx(records, twentysixidx)
    version3 = _copy_with_exclude_idx(records, youngestidx)
    return version1, version2, version3  # , oldest, youngest


def generate_data_for_exponential_mechanism(records):
    """
    generate data for Exponential Mechanism
    
    Arguments:
            records {[list of list]} -- [original dataset]
    """
    counter = {}
    eduidx = ATTNAME.index('education')
    for idx, record in enumerate(records):
        if record[eduidx] == '*':
            continue
        counter[record[eduidx]] = counter.get(record[eduidx], []) + [idx]

    firstlen, secondlen, leastlen = -float('inf'), -float('inf'), float('inf')
    firstedu, secondedu, leastedu = '', '', ''
    for key, val in counter.items():
        if len(val) > firstlen:
            secondlen = firstlen
            secondedu = firstedu
            firstlen = len(val)
            firstedu = key
        elif len(val) > secondlen:
            secondlen = len(val)
            secondedu = key
        if len(val) < leastlen:
            leastlen = len(val)
            leastedu = key
    firstidx = counter[firstedu][random.randrange(0, firstlen)]
    secondidx = counter[secondedu][random.randrange(0, secondlen)]
    leastidx = counter[leastedu][random.randrange(0, leastlen)]

    version1 = _copy_with_exclude_idx(records, firstidx)
    version2 = _copy_with_exclude_idx(records, secondidx)
    version3 = _copy_with_exclude_idx(records, leastidx)
    return version1, version2, version3


def _copy_with_exclude_idx(records, tgtidx):
    """
    generate a new list of records without the target idx: tgtidx
    
    Arguments:
            records {[list of list]} -- [original records]
            tgtidx {[int]} -- [target idx will be excluded from records]
    
    Returns:
            [list of list] -- [copy of records excluding the tgtidx record]
    """

    return [record for idx, record in enumerate(records) if idx != tgtidx]


def generate_hierarchy_for_age(records):
    youngest, oldest = float('inf'), -float('inf')
    ageidx = ATTNAME.index('age')
    for record in records:
        if record[ageidx] == -1:
            continue
        if record[ageidx] > oldest:
            oldest = record[ageidx]
        if record[ageidx] < youngest:
            youngest = record[ageidx]
    print('age max: %d min: %d' % (oldest, youngest))
    with open(AGECONFFILE, 'w') as wf:
        for i in range(oldest + 1):
            h = []
            h.append(str(i))
            #     h.append('%s-%s' %(i//10*10, (i//10+1)*10))
            #     h.append('%s-%s' %(i//20*20, (i//20+1)*20))
            #     h.append('%s-%s' %(i//50*50, (i//50+1)*50))
            #     h.append('%s-%s' %(i//100*100, (i//100+1)*100))
            h.append('%s-%s' % (i // 25 * 25, (i // 25 + 1) * 25))
            #     h.append('%s-%s' % (i//20*20, (i//20+1)*20))
            h.append('%s-%s' % (i // 50 * 50, (i // 50 + 1) * 50))
            h.append('%s-%s' % (i // 100 * 100, (i // 100 + 1) * 100))
            wf.write(','.join(h))
            wf.write('\n')


def generate_hierarchy_for_edu(records):
    eduset = set()
    eduidx = ATTNAME.index('education')
    for record in records:
        if record[eduidx] != '*' and record[eduidx] not in eduset:
            eduset.add(record[eduidx])
    with open(EDUCONFFILE, 'w') as wf:
        for edu in eduset:
            wf.write(edu + ',' * 2)
            wf.write('\n')


def generate_hierarchy_for_marital(records):
    maritalset = set()
    maritalidx = ATTNAME.index('marital-status')
    for record in records:
        if record[maritalidx] != '*' and record[maritalidx] not in maritalset:
            maritalset.add(record[maritalidx])
    with open(MARITALCONFFILE, 'w') as wf:
        for marital in maritalset:
            wf.write(marital + ',' * 2)
            wf.write('\n')


def generate_hierarchy_for_race(records):
    reaceset = set()
    raceidx = ATTNAME.index('race')
    for record in records:
        if record[raceidx] != '*' and record[raceidx] not in reaceset:
            reaceset.add(record[raceidx])
    with open(RACECONFFILE, 'w') as wf:
        for race in reaceset:
            wf.write(race + ',' * 2)
            wf.write('\n')


if __name__ == "__main__":
    print(os.getcwd())
    records = readdata()
    generate_hierarchy_for_age(records)
#     generate_hierarchy_for_edu(records)
#     generate_hierarchy_for_marital(records)
#     generate_hierarchy_for_race(records)
