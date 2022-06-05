import os
import pickle
import xlwt


def createXLSforNamadFromPkl(OutputDir="namads", InputFile="AllData.pkl"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    f = open(InputFile, "rb")
    allData = pickle.load(f)
    f.close()

    print('start writing results for ' + str(allData.__len__()) + ' namad')

    pr = 0
    for namad in allData:

        if os.path.exists(OutputDir + '/' + namad + '.xls'):
            continue

        book = xlwt.Workbook()

        namadPage = book.add_sheet(namad)
        c = 0
        for sotoon in allData[namad]:
            if sotoon == 'نام':
                continue

            # allData[namad][sotoon].sort(key=lambda k: k['pd'])
            namadPage.write(0, c + 2, sotoon)

            vals = allData[namad][sotoon]
            r = 1
            for v in vals:
                namadPage.write(r, c, v['pInWeek'])
                namadPage.write(r, c + 1, v['pd'].isoformat())
                # namadPage.write(r, c + 1, v['pd'])
                try:
                    namadPage.write(r, c + 2, int(v['v']))
                except:
                    namadPage.write(r, c + 2, '-')

                r += 1

            c += 3

        pr += 1
        print(str(int(pr / allData.__len__() * 100)) + '% ... namad: ' + namad + ' saved!')
        # if pr >10 :
        #     break

        book.save(OutputDir + '/' + namad + '.xls')


def groupNamadDataIntermOfDayOfWeekFromPKL(InputFile="AllData.pkl", OutputDir='namadsOnDayOfWeek'):
    f = open(InputFile, "rb")
    allData = pickle.load(f)
    f.close()

    print('start writing results for ' + str(allData.__len__()) + ' namad')

    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    pr = 0
    for namad in allData:

        if os.path.exists(OutputDir + '/' + namad + '.xls'):
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

        book.save(OutputDir + '/' + namad + '.xls')
        # for n in nparrays:
        #     directory = outDir+'/'+namad+'_asndarray/'
        #     if not os.path.exists(directory):
        #         os.makedirs(directory)
        #     nda = numpy.asanyarray(nparrays[n])
        #     numpy.save(directory+n ,nda)

        if pr > 10:
            break
