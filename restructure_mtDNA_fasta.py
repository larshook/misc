#!/usr/bin/env python
#
# Lars Höök, 2020 - lars.hook@ebc.uu.se
#
# Script that changes the starting gene of a circularized mitochondrial genome to trnM(atg).
# Takes a genome fasta and annotation bed file as input and outputs a new, restructured fasta.
# 
# Run: python restructure_mtDNA.py <mtDNA.fasta> <mtDNA.bed>
#
# TODO: take any input name as start position "--start_gene"
#

import sys
import pandas as pd
from Bio import SeqIO

fasta_file = sys.argv[1]
bed_file = sys.argv[2]

# read BED-file and get position of trnM(atg).
BED_file = pd.read_csv(bed_file, sep='\t', header=None)
BED_file.columns = ["ID", "Start", "End", "Gene", "P-val", "Strand"]
N_to_move = (BED_file.loc[BED_file['Gene'] == "trnM(atg)", 'Start'].iloc[0])

# Store fasta sequence
for seq_record in SeqIO.parse(fasta_file, "fasta"):
    SEQUENCE = seq_record.seq

# Rearrange sequence to start with trnM(atg)
START_SEQUENCE = SEQUENCE[N_to_move:]
END_SEQUENCE = SEQUENCE[0:N_to_move]

#print to new file
outputfile = fasta_file.split(".")[0]+"-rearranged.fasta"
HEADER = fasta_file.split(".")[0]
with open(outputfile, 'w') as f:
    print('>', HEADER, sep='', file=f)
    print(START_SEQUENCE, END_SEQUENCE, sep='', file=f)
