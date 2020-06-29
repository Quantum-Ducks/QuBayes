#!/bin/bash

# assumes you have global data csv downloaded from: 
# https://www.google.com/covid19/mobility/

# keep only the US, and only regions in the US
awk -F, '$1 == "US"' Global_Mobility_Report.csv | awk -F, '$5!=""' > US_Mobility_Reposrt.csv

# write retail/rec and work data for a specific week to a file (eg. june given here) 
awk -F, '{if ($7 ~ /2020-06-(1[4-9]|20)/) {print $3,",",$7,",",$8,",",$12}}' US_Mobility_Report.csv > june.csv

# pull out retail/recreation data for the four specified weeks, sort, and plot as a scatterplot
awk -F, '{if ($7 ~ /2020-03-2[2-8]/ || /2020-04-1[2-8]/ || /2020-05-1[0-6]/ || /2020-06-(1[4-9]|20)/) {print $8}}' US_Mobility_Report.csv | sort | gnuplot -e "set terminal png size 400,300; set output 'retailandrec_sorted.png'; plot '/dev/stdin'"

# save sorted work data as csv
awk -F, '{if ($7 ~ /2020-03-2[2-8]/ || /2020-04-1[2-8]/ || /2020-05-1[0-6]/ || /2020-06-(1[4-9]|20)/) {print $11}}' US_Mobility_Report.csv | sort > work.csv

# count number of values between two percentages
awk -F, '{if ($1 >= 0) print $1}' retailandrec.csv | wc -l
awk -F, '{if ($1 >= -53 && $1 < -26) print $1}' retailandrec.csv | wc -l







