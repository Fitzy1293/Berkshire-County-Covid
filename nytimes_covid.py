#!/bin/env python3

#![Imgur](https://i.imgur.com/CrzzuEZ.png)

from pprint import pprint
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys

def berkshireRows(file): # Parses CSVs
    head = ['date','county','state','fips','cases','deaths']

    file = open(file, 'r').read().splitlines()
    rows =  [head] + [i.rstrip(',').split(',')  for i in file if i.split(',')[1]=='Berkshire']

    return rows

def rowStr(rows):
    returnRows = []

    previous = rows[1]
    for i in rows[2:]:
        row = ['-'.join(i[0].split('-')[1:] + [i[0].split('-')[0]])]
        caseDiff = f'{i[-2]} ==> diff={int(i[-2]) - int(previous[-2])}'
        deathDiff = f'{i[-1]} ==> diff={int(i[-1]) - int(previous[-1])}'

        row.extend((caseDiff, deathDiff))
        returnRows.append(row)
        previous = i

    return returnRows

def plotCovid(rows):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]
    date = '/'.join(rows[-1][0].split('-')[1:] + [rows[-1][0].split('-')[0]])


    # Create 2x2 sub plots
    gs = gridspec.GridSpec(2, 2)

    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, 1]) # row 0, col 0
    ax1.plot(cases, 'r.-')
    ax1.set(xlabel='Days since 3/8/2020', ylabel='Cases',
           title='Berkshire County, MA - COVID-19 cases')

    ax2 = fig.add_subplot(gs[1, 1]) # row 0, col 1
    ax2.plot(deaths, 'm.')
    ax2.set(xlabel='Days since 3/8/2020', ylabel='Total deaths',
           title='Berkshire County, MA - COVID-19 deaths')
    ax2.plot([0,1])

    ax3 = fig.add_subplot(gs[:, 0]) # row 1, span all columns
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

    ax3.set(xlabel='Days since 3/8/2020', ylabel='COVID-19 cases and deaths',
           title=f'COVID-19 Tracking\nBerkshire County, MA\n3/8/2020 - {date}')


    fig.set_size_inches(15, 15)
    plt.savefig("COVID_plots.png", dpi = 100)



if __name__ == '__main__':
    if '-getdata' in sys.argv:
        os.system('curl "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv" | grep Berkshire > Berkshire_County_nytimes.csv')
        print('Curling NY times COVID-19 CSV')

    curledCsv = 'Berkshire_County_nytimes.csv'
    rows = berkshireRows(curledCsv)
    plotCovid(rows)


    finalRows = [['Date', 'Cases', 'Deaths']] + [i for i in reversed(rowStr(rows))]

    outputCsv = f'All_Berkshire_Data_Provided--{finalRows[1][0]}.csv'
    with open(outputCsv, 'w+') as f:
        for i in finalRows:
            f.write(','.join(i))
            f.write('\n')
