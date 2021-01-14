#!/bin/bash

# Lars Höök, 2020 - lars.hook@ebc.uu.se

# Split a multifasta and make a separate file from each entry.
# Puts the new files in folder named by input file name.
# NOT tested with complicated file or entry names.
# Run: ./split_multifasta_to_fasta.sh <fasta_file.fasta>

module load bioinfo-tools
module load samtools

FASTA="$1"

samtools faidx $FASTA

DIRECTORY=$(echo $FASTA | tr -d ".fasta" | tr -d ".fa")
mkdir $DIRECTORY

grep ">" $FASTA > tmp_entry_list.txt

while read line; do
ENTRY=$(echo $line | tr -d '>')
echo $ENTRY | xargs samtools faidx $FASTA > $DIRECTORY/$ENTRY.fasta
done <tmp_entry_list.txt

rm -f tmp_entry_list.txt
