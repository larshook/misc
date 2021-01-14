#!/bin/bash -l

#SBATCH ...

# Lars Höök, 2021 - lars.hook@ebc.uu.se

# Script (slurm) to calculate fraction of W (female) specific positions per assembly scaffolds.
# W specific position is defined as having coverage by female reads and not by male reads.
# Positions with male read coverage only are considered as noise and are kept as neutral.
# Positions without coverage are filtered out.
# Input is two bam files: male and female reads mapped to female assembly.


################## set paths ###################

FEMALE=		#sample name
BAM_MALE= 	#without extension
BAM_FEMALE=	#without extension
MAIN_PATH=	#path to folder with input files

################################################


module load bioinfo-tools
module load samtools/1.10

cp $MAIN_PATH/$BAM_MALE.bam $SNIC_TMP
cp $MAIN_PATH/$BAM_FEMALE.bam $SNIC_TMP

cd $SNIC_TMP

# use samtools to get per position read depth - http://www.htslib.org/doc/samtools-depth.html
samtools depth -aa $BAM_MALE.bam > $BAM_MALE.cov
samtools depth -aa $BAM_FEMALE.bam > $BAM_FEMALE.cov

# combine output to make coverage table
cut -f 3 "$BAM_FEMALE.cov" | paste "$BAM_MALE.cov" - > table

# remove row if both have zero depth
awk '$3 != 0 || $4 != 0' table > table_filtered

# count number of male zeros ($3) per scaffold ($1)
awk '{if ($3 == 0) count[$1 OFS $3]++} END {for (key in count) print key, count[key]}' table_filtered | awk '{print $1, $3}' | sort -V > zero_count

# count number of positions per scaffold after filtering
cut -f1 table_filtered | uniq -c | sed 's/^\s*//' | awk '{print $2, $1}' | sort -V > position_count

# append number of positions to zero_count and calculate fraction of female specific positions
awk 'NR==FNR{a[$1]=$2; next}{print $1, $2, a[$1], $4 = $2 / a[$1] }' position_count zero_count > table_final.txt

cp $SNIC_TMP/table_final.txt $MAIN_PATH/
