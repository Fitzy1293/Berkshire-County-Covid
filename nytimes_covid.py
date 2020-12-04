#!/bin/env python3
from pprint import pprint

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

if __name__ == '__main__':
    curledCsv = 'Berkshire_County_nytimes.csv'
    rows = berkshireRows(curledCsv)
    days = [i for i in reversed(rowStr(rows))]
    finalRows = [['Date', 'Cases', 'Deaths']] + days
    outputCsv = f'All_Berkshire_Data_Provided--{finalRows[1][0]}.csv'
    with open(outputCsv, 'w+') as f:
        for i in finalRows:
            f.write(','.join(i))
            f.write('\n')
