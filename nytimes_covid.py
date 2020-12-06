#!/bin/env python3

from pprint import pprint
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def berkshireRows(file):  # Parses CSVs
    head = ['date','county','state','fips','cases','deaths']
    file = open(file, 'r').read().splitlines()
    return [head] + [i.split(',')  for i in file]

def dateFormat(nytDate):
    return '/'.join(nytDate.split('-')[1:] + [nytDate.split('-')[0]])

# Gets the deltas between days for cases and deaths.
def shortenTable(rows):
    fixedFirstDay = [
                dateFormat(rows[1][0]),
                f'{rows[1][-2]} Δ={rows[1][-2]}',
                f'{rows[1][-1]} Δ={rows[1][-1]}'
                ]

    returnRows = [fixedFirstDay]

    previous = rows[1]
    for i in rows[2:]:
        row = [dateFormat(i[0])]
        caseDiff = f'{i[-2]}: Δ={int(i[-2]) - int(previous[-2])}'
        deathDiff = f'{i[-1]}: Δ={int(i[-1]) - int(previous[-1])}'

        row.extend((caseDiff, deathDiff))
        returnRows.append(row)
        previous = i

    return returnRows

def plotCovid(rows):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]

    startDate = dateFormat(rows[1][0])
    endDate = dateFormat(rows[-1][0])

    gs = gridspec.GridSpec(2, 2) # Create 2x2 sub plots

    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, 1]) # row 0, col 0
    ax1.plot(cases, 'r.-')
    ax1.set(xlabel=f'Days since {startDate}', ylabel='Cases',
           title='Berkshire County, MA - COVID-19 cases')

    ax2 = fig.add_subplot(gs[1, 1]) # row 0, col 1
    ax2.plot(deaths, 'm.')
    ax2.set(xlabel=f'Days since {startDate}', ylabel='Total deaths',
           title='Berkshire County, MA - COVID-19 deaths')
    ax2.plot([0,1])

    ax3 = fig.add_subplot(gs[:, 0]) # col 1, span all rows
    ax3.plot(cases, 'r')
    ax3.plot(deaths, 'm')
    plt.fill_between(np.arange(0, len(cases)), deaths, cases,
                 facecolor="orange", # The fill color
                 color='r',       # The outline color
                 alpha=0.2)
    plt.fill_between(np.arange(0, len(cases)), deaths,
                 facecolor="orange", # The fill color
                 color='m',       # The outline color
                 alpha=0.2)

    ax3.set(xlabel=f'Days since {startDate}', ylabel='COVID-19 cases and deaths',
           title=f'COVID-19 Tracking\nBerkshire County, MA\n{startDate} - {endDate}')

    fig.set_size_inches(15, 15)
    plt.savefig("COVID_plots.png", dpi = 100)

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
    plotCovid(rows)

    finalRows = [['Date', 'Cases (Total Δ=Daily Change)', 'Deaths (Total Δ=Daily Change)']] + [i for i in reversed(shortenTable(rows))]
    csvCreate(finalRows)
    os.system('csvtomd All_Berkshire_Data_Provided.csv > markdown_table.md')


    nytDate = dateFormat(rows[-1][0])

    print(f'Date NYT CSV: {nytDate}')
    print(f'Updating markdown_table.md and README.md for {nytDate}')
    os.system('cp README.md previous_README.md')
    updateReadme(nytDate)
    print('README.md is up to date')

