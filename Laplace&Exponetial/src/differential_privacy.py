from src import laplace_mechanism
from utilis.readdata import *
from src import exponential_mechanism
import math


def evaluate_laplace_mechanism(eps=[0.5, 1]):
    """
    Evaluate for Laplace Mechanism
    """
    recordsv0 = readdata()
    recordsv1, recordsv2, recordsv3 = generate_data_for_laplace_mechanism(recordsv0)

    res1000 = {e: [] for e in eps}
    # res4000 = {e: [] for e in eps}
    rmse = {e: 0 for e in eps}

    """
    evaluate for epsilon = 0.5 and 1 for 1000 queries
    """
    printsent = ['original data', 'data removed a record with the oldest age',
                 'data removed any record with age 26', 'data removed any record with the youghest age']
    i = 0
    for records in (recordsv0, recordsv1, recordsv2, recordsv3):
        print('############ Processing for {} ############'.format(printsent[i]))
        i += 1
        LampMec = laplace_mechanism.LaplaceMechanism(records)
        for e in eps:
            print('query 1000 results with epsilon = {}'.format(e))
            res1000[e].append(LampMec.query_with_dp(e, querynum=1000))
            # res4000[e].append(LampMec.query_with_dp(e, querynum=4000))
            rmse[e] = LampMec.calc_distortion(
                LampMec.query_with_dp(e, querynum=4000))

    print('\n')
    for e in eps:
        print('############ Prove the {}-indistinguishable'.format(e))
        for i in range(1, 4):
            tmpresij, tmpresji = laplace_mechanism.prove_indistinguishable(
                res1000[e][0], res1000[e][i])
            print('** {} ** OVER ** {} **:'.format(printsent[0], printsent[i]))
            print(tmpresij)
            print('** {} ** OVER ** {} **:'.format(printsent[i], printsent[0]))
            print(tmpresji)
            print('exp^e = {}'.format(math.exp(e)))
            print('\n')

    print('############ Measure the distortion (RMSE) ############')
    for e in eps:
        print('RMSE for e = {}: {}'.format(e, rmse[e]))
    print('Distortion of e=1 is smaller than e=0.5 ?: ', True if rmse[1] <= rmse[0.5] else False)
    del recordsv0
    del recordsv1
    del recordsv2
    del recordsv3


def evaluate_exponential_mechanism(eps=[0.5, 1]):
    """
    Evaulate for Exponential Mechanism
    """

    recordsv0 = readdata()
    recordsv1, recordsv2, recordsv3 = generate_data_for_exponential_mechanism(recordsv0)

    res1000 = {e: [] for e in eps}
    # res4000 = {e: [] for e in eps}
    dist = {e: 0 for e in eps}

    """
    evaluate for epsilon = 0.5 and 1 for 1000 queries
    """
    printsent = ['original data', 'data removed a record with most frequent education',
                 'data removed a record with second most frequent education',
                 'data removed any record with the least frequent education']
    i = 0
    for records in (recordsv0, recordsv1, recordsv2, recordsv3):
        print('############ Processing for {} ############'.format(printsent[i]))
        i += 1
        ExpMe = exponential_mechanism.ExponentialMechanism(records)
        for e in eps:
            print('query 1000 results with epsilon = {}'.format(e))
            res1000[e].append(ExpMe.query_with_dp(e, querynum=1000))
            # res4000[e].append(LampMec.query_with_dp(e, querynum=4000))
            dist[e] = ExpMe.calc_distortion(
                ExpMe.query_with_dp(e, querynum=4000))

    print('\n')
    for e in eps:
        print('############ Prove the {}-indistinguishable'.format(e))
        for i in range(1, 4):
            tmpresij, tmpresji = exponential_mechanism.prove_indistinguishable(
                res1000[e][0], res1000[e][i])
            print('** {} ** OVER ** {} **:'.format(printsent[0], printsent[i]))
            print(tmpresij)
            print('** {} ** OVER ** {} **:'.format(printsent[i], printsent[0]))
            print(tmpresji)
            print('exp^e = {}'.format(math.exp(e)))
            print('\n')

    print('############ Measure the distortion (1-precision) ############')
    for e in eps:
        print('distortion for e = {}: {}'.format(e, dist[e]))
    print('Distortion of e=1 is smaller than e=0.5 ?: ', True if dist[1] <= dist[0.5] else False)


if __name__ == "__main__":
    print("############################### Laplace Mechanism ###############################")
    evaluate_laplace_mechanism()
    print('\n')
    print("############################### Exponential Mechanism ###############################")
    evaluate_exponential_mechanism()
