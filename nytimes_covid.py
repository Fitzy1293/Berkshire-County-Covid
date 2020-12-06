#!/bin/env python3

from pprint import pprint
import os
import sys


import covid_plot

def berkshireRows(file):  # Parses CSVs
    head = ['date','county','state','fips','cases','deaths']
    file = open(file, 'r').read().splitlines()
    return [head] + [i.split(',')  for i in file]

def dateFormat(nytDate):
    return '/'.join(nytDate.split('-')[1:] + [nytDate.split('-')[0]])

def createNewRow(row, previous):
    cases = f'{row[-2]}: Δ={int(row[-2]) - int(previous[-2])}'
    deaths = f'{row[-1]}: Δ={int(row[-1]) - int(previous[-1])}'
    return [row[0], cases, deaths, row[1:]]

def shortenTable(rows):
    previous = rows[1][1:]
    fixedFirstDay = [dateFormat(previous[0]), f'{previous[-2]} Δ={previous[-2]}', f'{previous[-1]} Δ={previous[-1]}']
    returnRows = [fixedFirstDay]

    for i in rows[2:]:
        newRow = createNewRow(i, previous)
        returnRows.append(newRow[0:-1])
        previous = newRow[-1]

    return returnRows

def csvCreate(rows):
    with open('All_Berkshire_Data_Provided.csv', 'w+') as f:
        for i in rows:
            f.write(','.join(i))
            f.write('\n')

def updateReadme(nytDate):
    with open('README.md', 'w+') as f: # Don't want to directly write over it.
        f.write(f'# Berkshire County, Massachusetts COVID-19 data\n\n')
        f.write(f'**Most Recent Update: {nytDate}**\n\n')
        f.write('[Using the New York Time\'s covid tracker](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv)\n\n')
        f.write(f'![plots](COVID_plots.png)\n\n')
        f.write(f'# COVID daily data\n\n')

        f.write(''.join(open('markdown_table.md')))
        f.write('\n')

if __name__ == '__main__':
    curledCsv = 'Berkshire_County_nytimes.csv'

    if '-getdata' in sys.argv: # Used when actually updating
        endpoint = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        print('Curling NY times COVID-19 CSV\n')
        os.system(f'curl {endpoint} | grep Berkshire > {curledCsv}')
        print()

    rows = berkshireRows(curledCsv)
    covid_plot.plotCovid(rows)

    outputTable = [i for i in reversed(shortenTable(rows))]
    head = ['Date', 'Cases (Total Δ=Daily Change)', 'Deaths (Total Δ=Daily Change)']
    csvCreate([head] + outputTable)

    os.system('csvtomd All_Berkshire_Data_Provided.csv > markdown_table.md')

    nytDate = dateFormat(rows[-1][0])

    print(f'Date NYT CSV: {nytDate}')
    print(f'Updating markdown_table.md and README.md for {nytDate}')
    os.system('cp README.md previous_README.md')
    updateReadme(nytDate)
    print('README.md is up to date')
