import argparse
import time
import resource
import os, sys, pandas, numpy, pathlib
import CytoSig
from scipy import stats
from statsmodels.stats.multitest import multipletests

parser = argparse.ArgumentParser()
parser.add_argument('-E', "--expression_file", type=str, default=None, required=True, help="Gene expression file.")
parser.add_argument('-O', "--output_tag", type=str, default=None, required=True, help="Prefix for output files.")
parser.add_argument('-S', "--sample_type", type=str, default=None, required=False, help="Sample type name.")
parser.add_argument('-C', "--cell_type", type=str, default=None, required=False, help="Cell type name.")
parser.add_argument('-SF', "--sample_file", type=str, default=None, required=False, help="A file with sample type names.")
parser.add_argument('-CF', "--cell_file", type=str, default=None, required=False, help="A file with cell type names.")
args = parser.parse_args()

def read_expression(input_file):
    # read input
    try:
        f = os.path.basename(input_file)
        if f.find('.pickle') >= 0:
            print(f)
            expression = pandas.read_pickle(input_file)
        else:
            expression = pandas.read_csv(input_file, sep='\t', index_col=0)
    except:
        sys.stderr.write('Fail to open input file %s\n' % input_file)
        sys.exit(1)
    
    # gene and sample names must be unique
    assert expression.index.value_counts().max() == 1
    assert expression.columns.value_counts().max() == 1
    
    print('input matrix dimension', expression.shape)
    return expression

def load_Text(input_file):
    res = []
    file = open(input_file)
    while(True):
        line = file.readline().replace("\n", "")
        if not line:
            break
        res.append(line)
    file.close()
    return res

# Parse cell type name
if args.cell_type is None and args.cell_file is None:
    print("ERROR: cell type or cell file must be provide.\n")
    sys.exit(-1)

if args.cell_type is not None:
    cell_key = [args.cell_type]

if args.cell_file is not None:
    cell_key = load_Text(args.cell_file)

# parse sample type name
if args.sample_type is not None:
    sample_key = [args.sample_type]

if args.sample_file is not None:
    sample_key = load_Text(args.sample_file)

# find samples
expression = read_expression(args.expression_file)

subColumns = set()
for v in expression.columns:
    chunks = v.split('.')
    for key in cell_key:
        if key in chunks[0]:
            subColumns.add(v)
    if args.sample_type is None and args.sample_file is None:
        continue
    for key in sample_key:
        if key in chunks[1]:
            subColumns.add(v)

# output file
print("Found", len(subColumns), "samples.\n")

result = expression.loc[:, list(subColumns)]
result.to_csv(args.output_tag + '_subset.tsv', sep='\t', index_label='ID')
