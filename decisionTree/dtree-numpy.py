#!/usr/local/bin/python
# encoding: utf-8

# FIXME: extend this code to cover continuous variables
# TODO: when working column-wise, should i transpose the matrix first?

import sys
import os
import numpy as NP


class DecisionTree :

    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, gvid=None) :
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb
        self.gvid=gvid



nrows = 16

fnx = lambda l, h : NP.random.randint(l, h, nrows)

c1 = fnx(0, 4);c2 = fnx(0, 2);c3 = fnx(0, 10);c4 = fnx(0, 5);CL = fnx(1, 6)

# convert to list--real data will be in python nested list
D = NP.column_stack((c1, c2, c3, c4, CL)).tolist()


def entropy(rows) :
    from math import log
    log2 = lambda x : log(x) / log(2)
    results = unique(rows)
    ent=0.0
    for r in results.keys() :
        p = float(results[r]) / len(rows)
        ent -= p*log2(p)
    return ent


def wt_ave_var(arr1, arr2) :
    """
        returns weighted average variance of the two component slices
        of column array (the 'class_labels')
        arr1, arr2 1D NumPy arrays (two pieces of the column vector
        'class labels')
    """
    comb_len = float(len(arr1) + len(arr2))
    s1, s2 = len(arr1)/comb_len, len(arr2)/comb_len
    return s1*NP.var(arr1) + s2*NP.var(arr2)


####################################################################################
############### put the data in working form ##################
####################################################################################

#----------remove the class labels from the data-------------#
CL = [row[-1] for row in D]
D = [row[:-1] for row in D]

#------convert string representation to integer (column by column)-------#
# create LuT (data passed in here will be a nested python list)
# first, transpose the 2D python list so it's easier to work with
v = [ [row[col] for row in D] for col in range(len(D[0])) ]
v = [{x for x in v[i]} for i in range(len(v)) ]

##### LuTs for the data
# where 'kx' is a set (from the list of sets, above, v)
LuT0 = [ {k:v for k,v in zip(itm, range(len(itm)))} for itm in v ]
# *this LuT should be reversed & used downstream
LuT1 = [ {v:k for k,v in zip(itm, range(len(itm)))} for itm in v ]

##### LUTs for the class labels
LuT3 = { v:k for k,v in enumerate({x for x in cl}) }
LuT4 = { k:v for k,v in enumerate({x for x in cl}) }

# now that the LuTs are created, transform the data
# to a NumPy 2D array, dtype=int8



####################################################################################
############################## constructing the tree ###############################
####################################################################################


# now split W on the first value:
    # create the indices:
ndx1 = D[:,0] == 1
ndx0 = D[:,0] != 1

    # use the index to select the rows that satisfy the criterion
pos = D[ndx1,]      # just those rows that satisfy the splitting criterion
neg = D[ndx0,]      # the remainder of the rows from the data set (W)

# calculate the weighted average variance

# calculate var_wt for all unique values in a given column, and for
# all columns in the data matrix, D
sc_all = []
V = []
for i in range(D.shape[1]) :
    sc_all.append(NP.unique(D[:,i]))

for i, sc in enumerate(sc_all) :
    for j, itm in enumerate(sc) :
        ndx1 = D[:,i] == itm
        ndx0 = D[:,i] != itm
        var_wt = wt_ave_var(CL[ndx1], CL[ndx0])
        V.append((i, j, var_wt))
    print("\n")


# [test: flattened len(sc_all) must equal len(V)]
# now sort V based on last value (wt ave variance):
ndx = NP.argmin(V[:,-1])
V = V[ndx,]
