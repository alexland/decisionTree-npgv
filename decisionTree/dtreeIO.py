#!/usr/local/bin/python2.7
# encoding: utf-8

import sys
import os
import subprocess as SP
import shlex
import fileinput as FN
import argparse as AP


parser = AP.ArgumentParser(description='fileIO')
parser.add_argument('-i', metavar='N', action='store', dest='data_in',
                    help='the file that holds the data for input to dtree',)
parser.add_argument('-o', metavar='N', action='store', dest='tree_out')
args = parser.parse_args()

fname = args.data_in



