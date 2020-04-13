import sys
sys.path.append('../')
from utilis.readdata import *
from src.k_anonymity import KAnonymity

def main():
    records = readdata()
    K = [5, 10, 50, 100]
    KAnony = KAnonymity(records)
    for k in K:
        print('############# k-anonymity for k={} #############: \n'.format(k))
        KAnony.anonymize(k=k)
        print('\n')


if __name__ == "__main__":
    main()    
