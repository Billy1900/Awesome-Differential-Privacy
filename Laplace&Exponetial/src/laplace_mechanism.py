from utilis.readdata import *
import numpy as np
import math


class LaplaceMechanism():
    def __init__(self, records):
        self.records = records
        self.s = self.__calculate_sensitivity()
        # print(self.s)

    def __calculate_sensitivity(self):
        """
        calculate the sensitive value
        it should be the oldest age / num of records

        Returns:
            [float] -- [sensitive value]
        """

        num, oldage = 0, -float('inf')
        ageidx = ATTNAME.index('age')
        for record in self.records:
            if record[ageidx] > 25:
                num += 1
                if record[ageidx] > oldage:
                    oldage = record[ageidx]
        return oldage / num

    def __laplacian_noise(self, e):
        """
        add laplacian_noise
        """

        return np.random.laplace(self.s / e)

    def query_with_dp(self, e=1, querynum=1000):
        """
        query average age above 25 with Laplace Mechanism
        
        Keyword Arguments:
            e {float} -- [epsilon] (default: {1})
            querynum {int} -- [number of queries] (default: {1000})
        
        Returns:
            [list] -- [randomized query results]
        """

        ageidx = ATTNAME.index('age')
        agegt25 = [record[ageidx]
                   for record in self.records if record[ageidx] > 25]
        avgage = sum(agegt25) / len(agegt25)

        res = []
        for _ in range(querynum):
            res.append(round(avgage + self.__laplacian_noise(e), 2))
        return res

    def calc_groundtruth(self):
        """
        calculate the true average age above 25 without adding noise
        
        Returns:
            [float] -- [true average age greater than 25]
        """

        agesum = 0
        num = 0
        ageidx = ATTNAME.index('age')
        for record in self.records:
            if record[ageidx] > 25:
                agesum += record[ageidx]
                num += 1
        return round(agesum / num, 2)

    def calc_distortion(self, queryres):
        """
        calcluate the distortion
        use RMSE here
        
        Arguments:
            queryres {[list]} -- [query result]
        
        Returns:
            [float] -- [rmse value]
        """

        groundtruth = self.calc_groundtruth()
        rmse = (sum((res - groundtruth) ** 2 for res in queryres) / len(queryres)) ** (1 / 2)
        return rmse


def prove_indistinguishable(queryres1, queryres2, bucketnum=20):
    """
    prove the indistinguishable for two query results
    
    Arguments:
        queryres1 {[list]} -- [query 1 result]
        queryres2 {[list]} -- [query 2 result]
    
    Keyword Arguments:
        bucketnum {int} -- [number of buckets used to calculate the probability] (default: {20})
    
    Returns:
        [float] -- [probability quotient]
    """

    maxval = max(max(queryres1), max(queryres2))
    minval = min(min(queryres1), min(queryres2))
    count1 = [0 for _ in range(bucketnum)]
    count2 = [0 for _ in range(bucketnum)]
    for val1, val2 in zip(queryres1, queryres2):
        count1[math.floor((val1 - minval + 1) / ((maxval - minval + 1) / bucketnum)) - 1] += 1
        count2[math.floor((val2 - minval + 1) // ((maxval - minval + 1) / bucketnum)) - 1] += 1
    prob1 = list(map(lambda x: x / len(queryres1), count1))
    prob2 = list(map(lambda x: x / len(queryres2), count2))

    res1overres2 = sum(p1 / p2 for p1, p2 in zip(prob1, prob2) if p2 != 0) / bucketnum
    res2overres1 = sum(p2 / p1 for p1, p2 in zip(prob1, prob2) if p1 != 0) / bucketnum
    return res1overres2, res2overres1


if __name__ == "__main__":
    records = readdata()
    v1, v2, v3 = generate_data_for_laplace_mechanism(records)
    LapMe = LaplaceMechanism(records)
    res1 = LapMe.query_with_dp(0.5, 1000)
    print(res1)
    print(LapMe.calc_groundtruth())
    print(LapMe.calc_distortion(LapMe.query_with_dp(1, 1000)))
    LapMe2 = LaplaceMechanism(v1)
    res2 = LapMe2.query_with_dp(0.5, 1000)
    print(LapMe.calc_distortion(res1))
    print(LapMe2.calc_distortion(res2))
    print(prove_indistinguishable(res1, res2))
    print(prove_indistinguishable(res2, res1))
    print(math.exp(0.5))
