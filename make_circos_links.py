# 2021 Lars Höök - lars.hook@ebc.uu.se
#
# Script to transform alignment table into circos link input file.
# Designed to let user choose columns depending on different alignment input file formats
# Format for circos links file, describing an alignment between chr_1 of species a and b is:
#   'a_chr_1' 'start' 'end' 'b_chr_1' 'start' 'end' 'color(optional)'
#
# Identifier used for query/target should correspond with id used in karyotype file
# e.g: if karyotype id is ???_SCAFFOLD_N, set -q/-t to ???
#
# Run: python make_karyotype.py [-parameters] [-options]
#
# Required parameters:
# -a/--alignment [in.file]      alignment input file
# -o/--output_file [out.file]   output file
# -q/--query [name]             set query identifier - must match karyotype
# -t/--target [name]            set target identifier - must match karyotype
# -qc/--query_column [INT]      set query column
# -qs/--query_start [INT]       set query start
# -qe/--query_end [INT]         set query end
# -tc/--target_column [INT]     set target column
# -ts/--target_start [INT]      set target start
# -te/--target_end [INT]        set target end
#
# Options:
# -c/--color                    add color scale 'col_N' (default=off)
#
# TODO:
#  +/- alignments


import argparse
import pandas as pd
pd.options.mode.chained_assignment = None
import natsort as ns

parser=argparse.ArgumentParser()
parser.add_argument("-a", "--alignment", help="alignment input file", type=argparse.FileType('r'), required=True)
parser.add_argument("-o", "--output_file", help="output file", required=True)
parser.add_argument("-q", "--query", help="set query identifier - must match karyotype", type=str, required=True)
parser.add_argument("-t", "--target", help="set target identifier - must match karyotype", type=str, required=True)
parser.add_argument("-qc", "--query_column", help="set query column", type=int, required=True)
parser.add_argument("-qs", "--query_start", help="set query start", type=int, required=True)
parser.add_argument("-qe", "--query_end", help="set query end", type=int, required=True)
parser.add_argument("-tc", "--target_column", help="set target column", type=int, required=True)
parser.add_argument("-ts", "--target_start", help="set target start", type=int, required=True)
parser.add_argument("-te", "--target_end", help="set target end", type=int, required=True)
parser.add_argument("-c", "--color", help="add color scale 'col_N' (default=off)", action="store_true")
args=parser.parse_args()

# make new table based on arguments
df = pd.read_csv(args.alignment, sep="\s+|;|,", engine='python')

query = args.query_column-1
qstart = args.query_start-1
qend = args.query_end-1
target = args.target_column-1
tstart = args.target_start-1
tend = args.target_end-1

df_ = df.iloc[:, [query, qstart, qend, target, tstart, tend]]

# add tags to query and target scaffolds
df_.iloc[:, 0] = args.query + "_" + df_.iloc[:, 0]
df_.iloc[:, 3] = args.target + "_" + df_.iloc[:, 3]

# sort on query scaffolds, needed for color scale order to match karyotype input file
df_.iloc[:, 0] = pd.Categorical(df_.iloc[:, 0], ordered=True, categories= ns.natsorted(df_.iloc[:, 0].unique()))
df_ = df_.sort_values('Query')

# add color scale
if args.color:
    df_.insert(6, 'col', 'color=col_')
    df_['col'] = (df_['col'] + (df_.groupby('col').cumcount() + 1).astype(str))

# print to file
df_final=df_.to_csv(index=False, header=False, sep=' ')
with open(args.output_file, "w", newline='') as out_file:
    out_file.write(df_final)

#print(df_final)  #for testing
