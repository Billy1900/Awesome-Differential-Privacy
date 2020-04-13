# k-Anonymity

## 1. Introduction
To protect respondents’ identity when releasing microdata, data holders often remove or encrypt explicit identiflers, such as names and social security numbers. De-identifying data, however, provide no guarantee of anonymity. Released information often contains other data, such as race, birth date, sex, and ZIP code, that can be linked to publicly available information to re-identify respondents and to infer information that was not intended for release. One of the emerging concept in microdata protection is k-anonymity, which has been recently proposed as a property that captures the protection of a microdata table with respect to possible re-identiflcation of the respondents to which the data refer. k-anonymity demands that every tuple in the microdata table released be indistinguishably related to no fewer than k respondents. One of the interesting aspect of k-anonymity is its association with protection techniques that preserve the truthfulness of the data. In this chapter we discuss the concept of k-anonymity, from its original proposal illustrating its enforcement via generalization and suppression. We then survey and discuss research results on k-anonymity in particular with respect to algorithms for its enforcement. We also discuss difierent ways in which generalization and suppressions can be applied to satisfy k- anonymity and, based on them, introduce a taxonomy of k-anonymity solutions.

## 2. Configure

You can run the code just by `python k_anonymity.py` or `python kanonymity_eval.py` in directory `src`. Python 3.7 or Python 2.7 was tested successfully.

## 3. Theory

the code is based on the algorithm proposed from this paper [Link](https://github.com/Billy1900/Differential-Privacy/blob/master/k-Anonymity.pdf)
