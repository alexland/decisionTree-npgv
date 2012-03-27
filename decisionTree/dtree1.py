#!/usr/local/bin/python2.7
# encoding: utf-8


import sys
import os
import re
import random
import itertools
import numpy as NP
import pygraphviz as PV


class DecisionNode :

	def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, gvid=None) :
		self.col = col
		self.value = value
		self.results = results
		self.tb = tb
		self.fb = fb
		self.gvid=gvid
	


def split(data, column, value) :
	fnx = None
	if isinstance(value, int) or isinstance(value, float) :
		fnx = lambda row : row[column] >= value
	else:
		fnx = lambda row: row[column] == value
	set1 = [row for row in data if fnx(row)]
	set2 = [row for row in data if not fnx(row)]
	return (set1, set2)


def response_var_freq(data):
	"""
		returns a dictionary in which keys are the unique members of
		the data column corresponding to the response variable, and
		the values are the frequency of key;
		pass in the entire data set
	"""
	import collections as CL
	cn = CL.Counter()
	for row in data:
		cn[row[-1]] += 1
	return dict(cn)


def entropy(data) :
	from math import log
	log2 = lambda x : log(x) / log(2)
	results = response_var_freq(data)
	ent = 0.
	for r in results.keys() :
		p = float(results[r]) / len(data)
		ent -= p * log2(p)
	return ent


def construct_tree(data, scoref=entropy) :
	if len(data) == 0 :
	# if data.shape[0] == 0 | len(NP.unique(data[:,-1])) == 1:
		return DecisionNode()
	current_score = scoref(data)
	hi_gain = 0.0
	hi_criterion = None
	hi_sets = None
	column_count = len(data[0]) - 1
	for col in range(column_count) :
		column_values={}
		for row in data:
			column_values[row[col]] = 1
		for value in column_values.keys() :
			(set1, set2) = split(data, col, value)
			p = float(len(set1)) / len(data)
			gain = current_score - p*scoref(set1) - (1 - p)*scoref(set2)
			if gain > hi_gain and len(set1) > 0 and len(set2) > 0 :
				hi_gain = gain
				hi_criterion = (col, value)
				hi_sets = (set1, set2)
	if best_gain > 0 :
		trueBranch = construct_tree(hi_sets[0])
		falseBranch = construct_tree(hi_sets[1])
		return DecisionNode(col = hi_criterion[0],
							value = hi_criterion[1],
							tb = trueBranch,
							fb = falseBranch,
							gvid = random.randint(111, 999))
	else:
		results = response_var_freq(data)
		gvid = random.randint(111, 999)
		return DecisionNode(results=results, gvid=gvid)


def classify(observation, tree) :
	"""
		returns a class label;
		pass in an observation to be classified (detach label) & a trained tree
		Note: this function is not used in buiding/training the decision tree
	"""
	if tree.results != None :
		return tree.results
	else:
		v = observation[tree.col]
		branch = None
		if isinstance(v, int) or isinstance(v, float) :
			if v >= tree.value :
				branch = tree.tb
			else:
				branch = tree.fb
		else :
			if v == tree.value :
				branch = tree.tb
			else :
				branch = tree.fb
	return classify(observation, branch)

