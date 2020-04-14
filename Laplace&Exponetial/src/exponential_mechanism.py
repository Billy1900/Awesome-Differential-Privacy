import numpy as np
from utilis.readdata import *
from collections import Counter
import math


class ExponentialMechanism():
    """
    exponential mechanism
    
    """

    def __init__(self, records):
        self.records = records
        self.s = self.__calculate_sensitivity()
        self.__count_education_nums_prop()

    def __calculate_sensitivity(self):
        """
        calculate the sensitivity
        as the score function is #members, the sensitivity is 1
        
        Returns:
            [int] -- [sensitivity]
        """
        return 1

    def __count_education_nums_prop(self):
        """
        calculate the number and probability for education attribute
        """

        self.educnt = {}
        eduidx = ATTNAME.index('education')
        for record in self.records:
            self.educnt[record[eduidx]] = self.educnt.get(record[eduidx], 0) + 1
        self.eduprop = {}
        for key, val in self.educnt.items():
            self.eduprop[key] = val / len(self.records)

    def __exponential(self, u, e):
        """
        return exponential probability
        
        Arguments:
            u {[float]} -- [probability]
            e {[float]} -- [epsilon]
        
        Returns:
            [float] -- [exponential probability]
        """

        return np.random.exponential(e * u / (2 * self.s))

    def query_with_dp(self, e=1, querynum=1000):
        """
        query with Exponential Mechanism
        
        Keyword Arguments:
            e {float} -- [epsilon] (default: {1})
            querynum {int} -- [number of queries] (default: {1000})
        
        Returns:
            [list] -- [list of queries]
        """

        # candidate = list(self.educnt.keys())
        # candidatefreq = [self.educnt[k] for k in candidate]
        candidate = list(self.eduprop.keys())
        # print(candidate)
        # print([self.educnt[k] for k in candidate ])
        candidatefreq = [self.eduprop[k] for k in candidate]
        res = []
        for _ in range(querynum):
            weights = [self.__exponential(freq, e) for freq in candidatefreq]
            weights = [w / sum(weights) for w in weights]
            # print(weights)
            res.append(np.random.choice(candidate, p=weights))
        return res

    def calc_groundtruth(self):
        """
        calculate the groundtruth
        the most frequent education value
        
        Returns:
            [string] -- [most frequent education value]
        """

        eduidx = ATTNAME.index('education')
        return Counter([record[eduidx] for record in self.records if record[eduidx] != '*']).most_common(1)[0][0]

    def calc_distortion(self, queryres):
        """
        calculate the distortion
        
        Arguments:
            queryres {[list]} -- [query result]
        
        Returns:
            [float] -- [distortion]
        """

        return 1 - Counter(queryres)[self.calc_groundtruth()] / len(queryres)


def prove_indistinguishable(queryres1, queryres2):
    """
    proove the indistinguishable for two query results
    
    Arguments:
        queryres1 {[list]} -- [query 1 result]
        queryres2 {[list]} -- [query 2 result]
    
    Returns:
        [float] -- [probability quotient]
    """

    prob1 = Counter(queryres1)
    for key in prob1:
        prob1[key] /= len(queryres1)
    prob2 = Counter(queryres2)
    for key in prob2:
        prob2[key] /= len(queryres2)
    res = 0
    num = 0
    for key in prob1:
        if key not in prob2:
            print('no query result {} in query 2'.format(key))
            continue
        res += prob1[key] / prob2[key]
        num += 1
    res1overres2 = res / num

    res = 0
    num = 0
    for key in prob2:
        if key not in prob1:
            print('no query result {} in query 1'.format(key))
            continue
        res += prob2[key] / prob1[key]
        num += 1
    res2overres1 = res / num
    return res1overres2, res2overres1


if __name__ == "__main__":
    records = readdata()
    ExpMe = ExponentialMechanism(records)
    res1 = ExpMe.query_with_dp(0.05, 1000)
    # res2 = ExpMe.query_with_dp(0.05, 1000)
    v1, v2, v3 = generate_data_for_exponential_mechanism(records)
    ExpMe2 = ExponentialMechanism(v1)
    res2 = ExpMe2.query_with_dp(0.05, 1000)
    # print(res1)
    print(ExpMe.calc_distortion(res1))
    print(ExpMe.calc_distortion(ExpMe.query_with_dp(1, 1000)))
    print(ExpMe.calc_distortion(res2))
    print(prove_indistinguishable(res1, res2))
    print(prove_indistinguishable(res2, res1))
    print(math.exp(0.05))
