# do stuff with google mobility data 

# change csv file to dictionary
import csv
reader = csv.DictReader(open('US_Mobility_Report.csv'))

data = {}
for row in reader:
  for col, val in row.items(): 
        data.setdefault(col, []).append(val)

# check that columns are correct pls
#for key, val in data.items():
#  print(key)


# keep only US region data -- not counties
for entry in data:
  country = data.get('country_region_code')
  isocode = data.get('iso_3166_2_code')
  
  if country =! 'US':
    # US data only
    continue
  
  if isocode == '':
    # this row contains county data
    continue

  else:


# loop through region data
region = data.get('iso_3166_2_code')
print(region)



