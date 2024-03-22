import argparse
import time
import resource
import os, sys, pandas, numpy, pathlib
import CytoSig
from scipy import stats
from statsmodels.stats.multitest import multipletests

parser = argparse.ArgumentParser()
parser.add_argument('-G', "--geneset_file", type=str, default=None, required=True, help="A gene set file in GMT format.")
parser.add_argument('-O', "--output_tag", type=str, default=None, required=True, help="Prefix for output files.")
parser.add_argument('-S', "--signature_file", type=str, default=None, required=True, help="A signature file with gene symbols, one gene per line.")
parser.add_argument('-N', "--signature_name", type=str, default=None, required=False, help="The name of the signature.")
args = parser.parse_args()

# read gmt file
text = []
fin = open(args.geneset_file)
for line in fin:
	text.append(line.strip())
fin.close()

# read signature file
gs = []
fin = open(args.signature_file)
for line in fin:
	gs.append(line.strip())
fin.close()

# update name
if args.signature_name is None:
	gn = (args.signature_file).split('/')[-1].split('.')[0]
else:
	gn = args.signature_name
tmp = [gn, gn]
tmp.extend(gs)
gsText = '\t'.join(tmp)

# output
text.append(gsText)
OUT = open(args.output_tag + '.gmt', 'w')
for line in text:
	OUT.write(line + '\n')
OUT.close()
