#!/usr/local/bin/python2.7
# encoding: utf-8

import sys
import os
import random
import re
import pygraphviz as PV
import networkx as NX
import dtree as DT
import dtreeIO as IO

G = PV.AGraph(dpi='120', directed=True)

random.seed(111)


def render_tree(t) :
    if t.fb.results :
        # create edge between t - t.fb
        G.add_edge( LuT[t.col]+': '+str(t.value)+' '+str(t.gvid),
            str(t.fb.results)+' '+str(t.fb.gvid), label='F')
    else :
        # create edge between t - t.fb & call render_tree on t.fb
        G.add_edge( LuT[t.col]+': '+str(t.value)+' '+str(t.gvid),
            LuT[t.fb.col]+': '+str(t.fb.value)+' '+str(t.fb.gvid), label='F')
        render_tree(t.fb)
    if t.tb.results :
        # create edge between t - t.tb
        G.add_edge( LuT[t.col]+': '+str(t.value)+' '+str(t.gvid),
            str(t.tb.results)+' '+str(t.tb.gvid), label='T' )
    else :
        # create edge between t - t.fb & call render_tree on t.tb
        G.add_edge( LuT[t.col]+': '+str(t.value)+' '+str(t.gvid),
            LuT[t.tb.col]+': '+str(t.tb.value)+' '+str(t.tb.gvid), label='T' )
        render_tree(t.tb)


#-------------------------- data IO ----------------------#

def dataIn(fname):
    data = []
    ptn = r'^\W+'
    pat_obj = re.compile(ptn)
    fnx = lambda v : pat_obj.sub('', v)
    with open(fname, 'r') as f :
        for row in f.readlines() :
            row = fnx(row)
            if row != '':
                row = row.strip().split(',')
                data.append(row)
    return data


# either call this Module from the command line, passing in a data file, or
# place that file in the next line and bind it to variable, 'fname':

fname = '/Users/doug/Dropbox/Machine Learning/decisionTree/production code/data/fruit.csv'

if IO.fname:
    with open(fname, 'r') as f :
        data = [line.strip().split(',') for line in f.readlines()]
elif fname:
    data = dataIn(fname)

headers = data.pop(0)
LuT = dict([itm for itm in enumerate(headers)])
#----------------------------- build & render Tree -----------------------------#
tree = DT.construct_tree(data)
render_tree(tree)

#----------------------------- graph aesthetics -----------------------------#

# styling for terminal nodes (results nodes)
node_attr_names1 = "fontcolor style fixedsize fillcolor color".split()
node_attr_vals1 = "white filled false cornflowerblue cornflowerblue".split()
na_names_vals1 = zip(node_attr_names1, node_attr_vals1)

# default styling (middle nodes, degree 3))
node_attr_names3 = "fontcolor shape fillcolor color shape fontname fontsize style fixedsize".split()
node_attr_vals3 = "navy diamond darkgoldenrod1 darkgoldenrod1 diamond Arial 9 filled false".split()
na_names_vals3 = zip(node_attr_names3, node_attr_vals3)

# styling for root node
node_attr_names2 = "shape style fixedsize fillcolor color".split()
node_attr_vals2 = "invhouse filled false indianred2 indianred2".split()
na_names_vals2 = zip(node_attr_names2, node_attr_vals2)

for node in G.nodes_iter():
    for n, v in na_names_vals3:
        node.attr[n] = v

for node in G.nodes_iter():
    if G.degree(node) == 1:
        for n, v in na_names_vals1:
            node.attr[n] = v
    elif G.degree(node) == 2:
        for n, v in na_names_vals2:
            node.attr[n] = v

# style the edges
edge_attr_names = "fontsize arrowsize color fontsize fontname labelfloat fontcolor".split()
edge_attr_vals = "10 .5 darkslategray4 9 Arial true gray75".split()
ea_names_vals = zip(edge_attr_names, edge_attr_vals)
for edge in G.edges_iter():
    for n, v in ea_names_vals:
        edge.attr[n] = v

# additional editing of node labels for display
ptn0 = r'\s?\d{3}$'
pat_obj0 = re.compile(ptn0)
ptn1 = r'\{|\}|\''
pat_obj1 = re.compile(ptn1)
ptn2 = r"[{}']"
pat_obj2 = re.compile(ptn2)

for node in G.nodes_iter():
    if G.degree(node) != 1 :
        s = pat_obj0.sub('', node)
        node.attr['label'] = "<{0}:<BR/>{1}>".format(*s.split(":"))
    if G.degree(node) == 1 :
        s = pat_obj0.sub('', node)
        node.attr['label'] = pat_obj2.sub('', s)

G.write('/Users/doug/Desktop/dTree_240312.dot')

