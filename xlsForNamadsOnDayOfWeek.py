import os
import pickle

import numpy
import xlwt
import jdatetime

f = open("AllData.pkl", "rb")
allData = pickle.load(f)

print('start writing resaults for ' + str(allData.__len__()) + ' namad')

outDir = 'namadsOnDayOfWeek'
if not os.path.exists(outDir):
    os.makedirs(outDir)

pr = 0
for namad in allData:

    if os.path.exists(outDir + '/' + namad + '.xls'):
        continue

    book = xlwt.Workbook()
    DayOfWeekPage = {}
    DayOfWeekPageIdx = {}
    tarikh = {}
    sarsotoon = {}
    # nparrays = {}

    for diw in jdatetime.date.j_weekdays_fa:
        # DayOfWeekPage[diw] = {}
        DayOfWeekPage[diw] = book.add_sheet(diw)
        tarikh[diw] = True
        # nparrays[diw] = []

    c = 1
    for sotoon in allData[namad]:
        if sotoon == 'نام':
            continue

        vals = allData[namad][sotoon]

        for diw in jdatetime.date.j_weekdays_fa:
            DayOfWeekPageIdx[diw] = 1
            sarsotoon[diw] = True

        for v in vals:

            if sarsotoon[v['pInWeek']]:
                DayOfWeekPage[v['pInWeek']].write(0, c, sotoon)
                sarsotoon[v['pInWeek']] = False
            if tarikh[v['pInWeek']]:
                DayOfWeekPage[v['pInWeek']].write(0, 0, 'تاریخ')
                tarikh[v['pInWeek']] = False

            if c <= 1:
                DayOfWeekPage[v['pInWeek']].write(DayOfWeekPageIdx[v['pInWeek']], 0, v['pd'].isoformat())

            try:
                DayOfWeekPage[v['pInWeek']].write(DayOfWeekPageIdx[v['pInWeek']], c, int(v['v']))
                # nparrays[v['pInWeek']].append(int(v['v']))
            except:
                DayOfWeekPage[v['pInWeek']].write(DayOfWeekPageIdx[v['pInWeek']], c, '-')

            DayOfWeekPageIdx[v['pInWeek']] += 1

        c += 1

    pr += 1

    print(str(int(pr / allData.__len__() * 100)) + '% ... namad: ' + namad + ' saved!')

    book.save(outDir + '/' + namad + '.xls')
    # for n in nparrays:
    #     directory = outDir+'/'+namad+'_asndarray/'
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    #     nda = numpy.asanyarray(nparrays[n])
    #     numpy.save(directory+n ,nda)

    if pr > 10:
        break
