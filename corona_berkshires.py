#!/bin/env python3

from pprint import pprint
import traceback

'''
Data compiled from mass. coronavirus archive https://www.mass.gov/info-details/archive-of-covid-19-cases-in-massachusetts# Data taken before March 17 was released onlay as a word doc
Could not find 8/1/2020 through 8/18/2020 data due to a formatting change

Berkshire county data from:
    Zip files located below

        https://www.mass.gov/doc/covid-19-raw-data-december-2-2020/download
            12/2/2020 - 8/19/2020

        https://www.mass.gov/doc/covid-19-raw-data-july-31-2020/download
            7/31/2020 - 4/17/2020

Concatenated County.csv from both zips with just Berkshire county data.

'''

def berkshireRows(file): # Parses CSVs
    head = ['Date', 'County', 'case_diff', 'cases', 'new_deaths', 'deaths']

    file = open(file, 'r').read().splitlines()
    rows =  [head] + [i.rstrip(',').split(',')  for i in file if i.split(',')[1]=='Berkshire']

    return rows

'''
Note: Due to a planned data system upgrade DPH did not publish a COVID-19 Dashboard on Sunday, 8/23.
The 8/24 Dashboard includes information reported to DPH over the previous weekend (from 5 p.m. Friday, 8/21 through 8 a.m. Monday, 8/24) and so numbers are higher than usual daily reporting on that 8/24 Dashboard.

The code below initializes cells with a missing flag for the days with missing attributes.
'''

def aggregateDays(countyCsv):


    rows = berkshireRows(countyCsv)

    rowCorrect = []
    for i in rows:
        if len(i) < 6:
            if len(i) == 4:
                correct = i[:2] + ['missing'] + [i[2]] + ['missing'] + [i[-1]]
            else:
                correct = i[:2] + ['missing'] + [i[2]] + ['missing'] + ['missing']
            rowCorrect.append(correct)
        else:
            rowCorrect.append(i)

    # Shell redirect to Berkshire_covid.csv for breivity
    with open('Berkshire_covid.csv', 'w+') as f:
        for i in rowCorrect:
            f.write(','.join(i) + '\n')

def getCaseDiff(day, previous, detail='COVID DETAIL'):
    missingCt = day.count('missing')
    if missingCt in (2, 3):
        try:
            diff = int(day[3]) - int(previous[3])
            fixed = day[:2] + [str(diff)] + day[3:]
            if missingCt == 3:
                return fixed
            else:
                diff = int(fixed[-1]) - int(previous[-1])
                #print(fixed, diff)
                return fixed[:4] + [str(diff)] + [fixed[-1]]
        except:
            #print(traceback.print_exc())
            return day

    else:
        return day

def mostRecentDay(latestDay):
    return latestDay[0].replace('/', '-')

def caseDiffs(berkshieCsv): # Getting diff from previous days count.
    days = berkshireRows(berkshieCsv)
    fixedDiffs = []
    previous = days[0]
    for i, day in enumerate(days):
        try:
            diffReturn = getCaseDiff(day, previous, detail='cases')
            fixedDiffs.append(diffReturn)
        except:
            pass#print(traceback.extract_exc())
        previous = day

    fname = f'All_Berkshire_Data_Provided--{mostRecentDay(fixedDiffs[-1])}.csv'
    with open(fname, 'w+') as f:
        f.write(','.join(fixedDiffs[0]) + '\n')
        for i in reversed(fixedDiffs[1:]):
            f.write(','.join(i) + '\n')

    print(f'Normalized row data:\t {fname}')

if __name__ == '__main__':
    print('Parsing data from https://www.mass.gov/info-details/archive-of-covid-19-cases-in-massachusetts ...')
    aggregateDays('County.csv')
    caseDiffs('Berkshire_covid.csv')
