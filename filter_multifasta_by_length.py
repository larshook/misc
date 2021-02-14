#!/usr/bin/env python
#
# Lars Höök, 2021 - lars.hook@ebc.uu.se
#
# Script to filter a multifasta on entry length
# Run: python filter_multifasta_by_length.py <infile> <outfile> -c [INT] [-options]
#
# Parameters:
# -c/--cutoff [INT]     entries below this cutoff will be removed
#
# Options:
# -m/--megabases        apply cutoff (-c) in megabases
# -a/--above            remove entries above cutoff (default=below)

import sys
import argparse
from Bio import SeqIO

parser=argparse.ArgumentParser()
parser.add_argument('files', nargs='*')
parser.add_argument("-c", "--cutoff", help="entries below this cutoff will be removed", type=float, required=True)
parser.add_argument("-m", "--megabases", help="apply cutoff (-c) in megabases", action="store_true")
parser.add_argument("-a", "--above", help="remove entries above cutoff (default=below)", action="store_true")
args=parser.parse_args()

fasta_file = sys.argv[1]
out_file = sys.argv[2]
scaffolds = []

if args.megabases:
    cutoff = args.cutoff*1000000
else:
    cutoff = args.cutoff

if args.above:
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        if len(seq_record) < cutoff:
            scaffolds.append(seq_record)
else:
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        if len(seq_record) > cutoff:
            scaffolds.append(seq_record)

SeqIO.write(scaffolds, out_file, "fasta")
