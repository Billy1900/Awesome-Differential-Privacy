from utilis.readdata import *


class KAnonymity():
    def __init__(self, records):
        self.records = records
        self.confile = [AGECONFFILE, EDUCONFFILE, MARITALCONFFILE, RACECONFFILE]

    def anonymize(self, qi_names=['age', 'education', 'marital-status', 'race'], k=5):
        """
        anonymizer for k-anonymity
        
        Keyword Arguments:
            qi_names {list} -- [qi names] (default: {['age', 'education', 'marital-status', 'race']})
            k {int} -- [value for k] (default: {5})
        """

        domains, gen_levels = {}, {}
        qi_frequency = {}  # store the frequency for each qi value
        # record_att_gen_levels = [[0 for _ in range(len(qi_names))] for _ in range(len(self.records))]

        assert len(self.confile) == len(qi_names), 'number of config files  not equal to number of QI-names'
        generalize_tree = dict()
        for idx, name in enumerate(qi_names):
            generalize_tree[name] = Tree(self.confile[idx])

        for qiname in qi_names:
            domains[qiname] = set()
            gen_levels[qiname] = 0

        for idx, record in enumerate(self.records):
            qi_sequence = self._get_qi_values(record[:], qi_names, generalize_tree)

            if qi_sequence in qi_frequency:
                qi_frequency[qi_sequence].add(idx)
            else:
                qi_frequency[qi_sequence] = {idx}
                for j, value in enumerate(qi_sequence):
                    domains[qi_names[j]].add(value)

        # iteratively generalize the attributes with maximum distinct values
        while True:
            # count number of records not satisfying k-anonymity
            negcount = 0
            for qi_sequence, idxset in qi_frequency.items():
                if len(idxset) < k:
                    negcount += len(idxset)

            if negcount > k:
                # continue generalization, since there are more than k records not satisfying k-anonymity
                most_freq_att_num, most_freq_att_name = -1, None
                for qiname in qi_names:
                    if len(domains[qiname]) > most_freq_att_num:
                        most_freq_att_num = len(domains[qiname])
                        most_freq_att_name = qiname

                # find the attribute with most distinct values
                generalize_att = most_freq_att_name
                qi_index = qi_names.index(generalize_att)
                domains[generalize_att] = set()

                # generalize that attribute to one higher level
                for qi_sequence in list(qi_frequency.keys()):
                    new_qi_sequence = list(qi_sequence)
                    new_qi_sequence[qi_index] = generalize_tree[generalize_att].root[qi_sequence[qi_index]][0]
                    new_qi_sequence = tuple(new_qi_sequence)

                    if new_qi_sequence in qi_frequency:
                        qi_frequency[new_qi_sequence].update(
                            qi_frequency[qi_sequence])
                        qi_frequency.pop(qi_sequence, 0)
                    else:
                        qi_frequency[new_qi_sequence] = qi_frequency.pop(qi_sequence)

                    domains[generalize_att].add(new_qi_sequence[qi_index])

                gen_levels[generalize_att] += 1


            else:
                # end the while loop
                # suppress sequences not satisfying k-anonymity
                # save results and calculate distoration and precision
                genlvl_att = [0 for _ in range(len(qi_names))]
                dgh_att = [generalize_tree[name].level for name in qi_names]
                datasize = 0
                qiindex = [ATTNAME.index(name) for name in qi_names]

                # used to make sure the output file keeps the same order with original data file
                towriterecords = [None for _ in range(len(self.records))]
                with open('../data/adult_%d_kanonymity.data' % k, 'w') as wf:
                    for qi_sequence, recordidxs in qi_frequency.items():
                        if len(recordidxs) < k:
                            continue
                        for idx in recordidxs:
                            record = self.records[idx][:]
                            for i in range(len(qiindex)):
                                record[qiindex[i]] = qi_sequence[i]
                                genlvl_att[i] += generalize_tree[qi_names[i]].root[qi_sequence[i]][1]
                            record = list(map(str, record))
                            for i in range(len(record)):
                                if record[i] == '*' and i not in qiindex:
                                    record[i] = '?'
                            towriterecords[idx] = record[:]
                            # wf.write(', '.join(record))
                            # wf.write('\n')
                        datasize += len(recordidxs)
                    for record in towriterecords:
                        if record is not None:
                            wf.write(', '.join(record))
                            wf.write('\n')
                        else:
                            wf.write('\n')

                print('qi names: ', qi_names)
                # precision = self.calc_precission(genlvl_att, dgh_att, datasize, len(qi_names))
                precision = self.calc_precision(genlvl_att, dgh_att, len(self.records), len(qi_names))
                distoration = self.calc_distoration([gen_levels[qi_names[i]] for i in range(len(qi_names))], dgh_att,
                                                    len(qi_names))
                print('precision: {}, distoration: {}'.format(precision, distoration))
                break

    def calc_precision(self, genlvl_att, dgh_att, datasize, attsize=4):
        """
        calculate the precision of generalized value for each value of each attributes
        
        Arguments:
            genlvl_att {[list]} -- [sum of generalized level of each attribute]
            dgh_att {[list]} -- [maximum height of each attribute]
            datasize {[int]} -- [data size]
        
        Keyword Arguments:
            attsize {int} -- [number of qi attributes] (default: {4})
        
        Returns:
            [float] -- [precision of the generalization]
        """

        return 1 - sum([genlvl_att[i] / dgh_att[i] for i in range(attsize)]) / (datasize * attsize)

    def calc_distoration(self, gen_levels_att, dgh_att, attsize):
        """
        calculate the distoration for generalized levels of each attributes
        
        Arguments:
            gen_levels_att {[type]} -- [description]
            dgh_att {[type]} -- [description]
            attsize {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """

        print('attribute gen level:', gen_levels_att)
        print('tree height:', dgh_att)
        return sum([gen_levels_att[i] / dgh_att[i] for i in range(attsize)]) / attsize

    def _get_qi_values(self, record, qi_names, generalize_tree):
        """
        private method
        get qi values from one record
        
        Arguments:
            record {[list]} -- [one record]
            qi_names {[list]} -- [qi names]
            generalize_tree {[dict]} -- [dict storing the DGH trees]
        
        Returns:
            [tuple] -- [qi tuple value]
        """

        qi_index = [ATTNAME.index(name) for name in qi_names]
        seq = []
        for idx in qi_index:
            if idx == ATTNAME.index('age'):
                if record[idx] == -1:
                    seq.append('0-100')
                else:
                    seq.append(str(record[idx]))
            else:
                if record[idx] == '*':
                    # TODO, handle missing value cases
                    record[idx] = generalize_tree[qi_names[idx]].highestgen
                seq.append(record[idx])
        return tuple(seq)


class Tree:
    """
    Tree class
    built for DGH tree, keep track of each node's parent, and current level
    """

    def __init__(self, confile):
        self.confile = confile
        self.root = dict()
        self.level = -1
        self.highestgen = ''
        self.buildTree()

    def buildTree(self):
        """
        build the DGH tree from config file
        """

        with open(self.confile, 'r') as rf:
            for line in rf:
                line = line.strip()
                if not line:
                    continue
                line = [col.strip() for col in line.split(',')]
                height = len(line) - 1
                if self.level == -1:
                    self.level = height
                if not self.highestgen:
                    self.highestgen = line[-1]
                pre = None
                for idx, val in enumerate(line[::-1]):
                    self.root[val] = (pre, height - idx)
                    pre = val


if __name__ == "__main__":
    records = readdata()
    KAnony = KAnonymity(records)
    KAnony.anonymize(k=100)
