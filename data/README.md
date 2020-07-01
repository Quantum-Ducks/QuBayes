# Data Wrangling

This folder contains scripts to collect and pre-process data, as well as csv files with data obtained from various sources and reorganized for our model to use.


### Sources for Data:
- [NY Times Stay at Home Orders](https://www.nytimes.com/interactive/2020/us/coronavirus-stay-at-home-order.html)

- [NY Times Reopening Data](https://www.nytimes.com/interactive/2020/us/states-reopen-map-coronavirus.html?auth=login-email&login=email)

- [Google Mobility Data](https://www.google.com/covid19/mobility/)

- [Johns Hopkins Testing Data](https://coronavirus.jhu.edu/testing/individual-states/florida)

- [NIH Confirmed Cases and Deaths](https://datascience.nih.gov/covid-19-open-access-resources)

- [CDC Health conditions at high risk for Covid](https://www.cdc.gov/mmwr/volumes/69/wr/mm6924e2.htm)
  
- [CDC Heart Disease Mortality Data](https://www.cdc.gov/nchs/pressroom/sosmap/heart_disease_mortality/heart_disease.htm)
  
- [CDC Diabetes Data](https://nccd.cdc.gov/Toolkit/DiabetesBurden/Prevalence)

- [CDC COPD Data](https://www.cdc.gov/copd/data.html)

- [Kaiser Family Foundation Race Demographics Data](https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?currentTimeframe=0&selectedDistributions=white&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D)

- [USDA Economic Research Service Poverty Rate Data](https://data.ers.usda.gov/reports.aspx?ID=17826)

- [masks4all State Mask Requirement Data](https://masks4all.co/what-states-require-masks/)

- [Kaiser Family Foundation Age Demographic Data](https://www.kff.org/other/state-indicator/distribution-by-age/?currentTimeframe=0&selectedDistributions=65&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D)


### Description of States Our Models Use:

Data for each variable was compliled from the sources above for each of the 50 US States. All variables except the last four (Age, racial demographics, poverty demographics and health demographics) were recorded for the weeks of March 22-28, April 12-18, May 10-16, and June 14-20 (all 2020).

- Stay At Home Order: 2 states. |1> = statewide stay at home order in place. |0> = no statewide stay at home order in place.

- Testing Availability: 2 states. |1> = ≤5% of tests come back positive in a 7 day average (the World Health Organization recommends testing enough of the      population to get below 5% positive). |0> = > 5% tests come back positive. 

- Cases: 2 states (Lesser model). |1> = Decreasing or flat from five day average at beginning of week to five day average at end of week |0> = Increasing from five day average at beginning of week to five day average at end of week

         4 states (Mallard and Alabio models). |3> = Decreasing or flat from five day average at beginning of week to five day average at end of week. |2> = Less than 10% increase from five day average at beginning of week to five day average at end of week. |1> = 10-50% increase from five day average at beginning of week to five day average at end of week. |0> = Greater than 50% increase from five day average at beginning of week to five day average at end of week

- Mask Order: 2 states. |1> = Statewide mask order in place. |0> = no statewide mask order in place.

- Travel to work and recreation: 4 states. |0> = More than 53% decrease from baseline Jan-Feb 2020. |1> = 26-53% decrease from baseline Jan-Feb 2020. |2> = Decrease of less than 26% from baseline Jan-Feb 2020. |3> = Increase from baseline Jan-Feb 2020.

- Death numbers: 2 states. |1> = Decreasing or flat from five day average at beginning of week to five day average at end of week |0> = Increasing from five day average at beginning of week to five day average at end of week

- Age of population: 2 states. |1> = Fraction of US state's population above 

- Racial minority population: 4 states. 

- Population living in poverty: 4 states. 

- Population with underlying health conditions: 4 states.



