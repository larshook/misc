#!/usr/bin/env python
#
# From biopython tutorial and cookbook
#
# Pick entries from multifasta based on list
# Run: python pick_scaffolds_from_multifasta.py <fasta_file.fasta> <list_file> <out_file>

from Bio import SeqIO
import sys

FASTA_FILE = sys.argv[1]
LIST_FILE = sys.argv[2]
SCAFFOLD_FILE = sys.argv[3]

with open(LIST_FILE) as id_handle:
    wanted = set(line.rstrip("\n").split(None, 1)[0] for line in id_handle)
print("Found %i unique identifiers in %s" % (len(wanted), LIST_FILE))

records = (r for r in SeqIO.parse(FASTA_FILE, "fasta") if r.id in wanted)
count = SeqIO.write(records, SCAFFOLD_FILE, "fasta")
print("Saved %i records from %s to %s" % (count, FASTA_FILE, SCAFFOLD_FILE))
if count < len(wanted):
    print("Warning %i IDs not found in %s" % (len(wanted) - count, FASTA_FILE))
