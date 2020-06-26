#!/bin/bash

# assumes you have global data csv downloaded from: 
# https://www.google.com/covid19/mobility/


# keep only the US, and only regions in the US
awk -F, '$1 == "US"' Global_Mobility_Report.csv | awk -F, '$5!=""' > US_Mobility_Reposrt.csv





