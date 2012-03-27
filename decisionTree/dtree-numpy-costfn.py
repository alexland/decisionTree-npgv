#------------------------ Entropy Calculation ------------------------#

# p(i) = frequency(outcome) = count(outcome) / count(total_rows)
# entropy = sum of p(i) x log2(p(i))

# synthetic class labels--3 unique labels, 25 data points
x = NP.random.randint(0, 2, 25)

ue = NP.unique(x)
p, entropy = 0., 0.
for itm in ue :
    ndx = row == itm
    p += NP.size(x[ndx]) / float(x.size)
    entropy -= p * log2(p)


def entropy(arr1) :
    import numpy as NP
    ue = NP.unique(x)
    p, entropy = 0., 0.
    for itm in ue :
        ndx = arr1 == itm
        p += NP.size(x[ndx]) / float(x.size)
        entropy -= p * NP.log2(p)
    return entropy
