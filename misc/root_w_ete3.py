#! /usr/bin/env python

#load libs
import os
import argparse
from ete3 import Tree

'''
#to keep the taxon ids as is
python3 root_w_ete3.py -tree UndinMarkers_DPANNEvo_503taxa_no_gappy_seq_clean.treefile -o test.tree -nototgr Asgard -outgroup_list my_list

#to shorten the taxon ids
python3 root_w_ete3.py -tree UndinMarkers_DPANNEvo_503taxa_no_gappy_seq_clean.treefile -o test.tree -nototgr Asgard -outgroup_list my_list -shorten
'''

#Argparse section
parser = argparse.ArgumentParser(description='root species tree and remove double bootstrap from iqtree output')
parser.add_argument('-tree','--treefile', metavar='list', required = True, help='list of taxa to use as outgroup')
parser.add_argument('-nototgr','--nototgr', metavar='str', required = True, help='taxon not in outgroup. Can be part of the taxon label, i.e. Asgard')
parser.add_argument('-outgroup_list','--outgroup', metavar='list', help='1 column list with taxa labels that are in the ancestor we want to root with. Needs to be the full taxon label and ensure that there  is no whitespace at the end of the file', required = True)
parser.add_argument('-shorten', "--shorten", action="store_true", help='Shorten taxon labels and only print GCA ID. This assumes taxon levels are separated with an - and have a total of 9 elements')
parser.add_argument('-o','--output', metavar='FASTA', help='multifasta file in with non-redundant sequences', required = True)
args = parser.parse_args()

if args.treefile is None and not os.path.exists(args.input):
    print("Treefile is missing!")
    sys.exit(-1)

#Global variables
Infile=args.treefile
Rooting_list = args.outgroup

#load tree
tree = Tree(Infile, format = 1)

#read in outgroups
anc_list = []
with open(Rooting_list) as f:
        for line in f:
            anc_list = f.read().splitlines() 

#define function to split taxa labels (assuming levels are separated with - and we have 9 elements in total)
def split_taxa():
    for node in tree.traverse(): 
        if node.is_leaf():
            node.name=node.name.split("-")[8].replace("_","-")

#manually load support labels (not needed for code below but maybe useful)
#if the label is 90/100 the code below takes the first element, i.e. 90
#we need the if statement, because the root has no support value and thus is ''
for node in tree.traverse():
    if not node.is_leaf():
        if node.name.split("/")[0] != '':
            node.support = float(node.name.split("/")[0])

#get list of tip labels
leaves = [tree.name for tree in tree.get_leaves()][::-1]

#to deal with trees being rooted by default in ete3 we reroot in a lineage we DON'T want to be in the outgroup first
sub = args.nototgr
reroot = [s for s in leaves if sub in s][0]
tree.set_outgroup(reroot)

#set root using our list of taxa in the ancestor
anc = tree.get_common_ancestor(anc_list)
tree.set_outgroup(anc)

#shorten taxon names (optional)
if args.shorten:
    split_taxa()
else:
    print("kept original ids")

#write tree to file
tree.write(outfile=args.output, format=0)
