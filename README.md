# Final Project Proposal
*High level summary of your project, including the things that* **you** *find interesting.*
My project aims to show how poverty among the country changes while the overall crime
of the US changes.
I find it interesting that quality of life has such a strong impact on social behavior. I also
find .gifs of heat maps representing real life things interesting to look at and think that
they give good look into trends.

## Data Plan
*Summarize data sources, data formats, and how to obtain or generate the data you will be using*
1. Small Area Income and Poverty Estimates (SAIPE) from the US Census Bureau.
- It contains poverty estimates for each county in the US by year.


2. Uniform Crime Reports for the entire nation
- A .csv of total crimes and crime rates in the US. By the FBI.

- The SAIPE data is only consistent from 1999 to 2015 and the UCR data goes until 2014, so it's best to use this for any period between 1999 and 2014 so a continuous .gif will be made

## Implementation Plan
*Overview of your plan. Are you starting from existing code? What skills from the course will be used to complete your project? etc.*
- The only existing code I will be using is from Lab 6 (Purple America) so I may generate the map of the United States
- The skills from the course I will be using are plotting, opening and reading files, and graph creations and
- I plan to map the United States and each state's county, and create visualizations of poverty in each county by using poverty data in those areas (taken from US Census Bureau). Also, beside the map, there will be a
graph of crime rate in the US for both violent and property crime

### External Libraries
- sys
- math
- matplotlib
- asn1crypto==0.22.0
- cffi==1.10.0
- cryptography==1.8.1
- cycler==0.10.0
- idna==2.5
- matplotlib==2.0.2
- packaging==16.8
- Pillow==4.1.1
- requests==2.14.2
- six==1.10.0
- urllib3==1.21.1


### Milestones
- Represent poverty and crime statistics in a .gif heat map of the US and a line graph
- Show the progression of those features throughout time

## Deliverables
- crime_poverty.py (the main script)
- .gif map of violent and property crime rates and poverty rates in the US

# Final Project Report
*What you have achieved/learned*
- manipulate data (even confusingly stored data)
- create .gifs and operate ImageMagick
- a better understanding of dictionaries, importance of creating multiple functions to complete a task, familiarity with the requests and matplotlib library
-

*What open questions remain*
- I saw that as the years went by, the overall crime rates tended to decrease. But, it looked (from the .gif) that select areas
 had increasing rates of crime. It's something I would like to look into in the future


## Instructions to run the code
1. Download the repo
2. Install the module libraries with pip
3. Enter in the terminal: `python3 crime_poverty.py statistic-data/crimes/USCrimeRates.csv statistic-data/poverty/PovertybyCounty.csv statistic-data/boundaries/US.csv 1024`
4. Install ImageMagick using brew: `update brew && brew install ImageMagick`
5. Enter in the terminal: convert `-delay 120 -loop 30 *stitched.png US.gif`
