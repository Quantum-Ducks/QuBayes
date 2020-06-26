# do stuff with google mobility data 

# change csv file to dictionary
import csv
reader = csv.DictReader(open('US_Mobility_Report.csv'))

data = {}
for row in reader:
    for col, val in row.items(): 
        result.setdefault(col, []).append(val)

# check that columns are correct pls
for key, val in result.items():
  print(key)






