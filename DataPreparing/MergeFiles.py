import jdatetime
import numpy
import pandas
import os
import pickle


# To merge daily xls files to python dictionary. Output is sorted interm of persian date
def mergeIranbourseAllDayExcelsByNamads(InputDir="DailyExcelsFromIranBourse", OutputFile="AllDataByNamad.pkl"):
    jdatetime.set_locale('fa_IR')

    allData = {}
    # if not os.path.exists(InputDir):
    #     os.makedirs(InputDir)

    for root, dirs, files in os.walk(InputDir):
        files.sort()
        print('start readin files')
        fi = 0.0
        for filename in files:
            print(str(int(fi / files.__len__() * 100.0)) + ' %  ... ' + filename)
            fi += 1.0
            try:
                df_list = pandas.read_html(InputDir + '/' + filename)
            except ValueError as e:
                if e.args[0] == 'No tables found':
                    continue
                else:
                    raise e

            if len(df_list) < 1:
                print('no Data Frame in > ' + filename)
                continue

            df = df_list[0]  # first frame only !
            # df.to_csv('DataPreparing/Data/table {}.csv'.format(0))
            if df.isnull().values.any():
                print('null value in > ' + filename)
                continue

            date = filename.split('.')[0].split('_')
            pd = jdatetime.date(int(date[1]), int(date[2]), int(date[3]))
            ed = pd.togregorian()
            dayInWeek = ed.strftime("%A")
            pdayInWeek = pd.strftime("%A")

            namadha = df['نماد'].values
            for sotoon in df.dtypes.index.values:
                # if t == 'نام' or t == 'نماد' :
                if sotoon == 'نماد':
                    continue
                # n =df[t].values
                i = 0
                for meqdar in df[sotoon].values:
                    if namadha[i] not in allData:
                        allData[namadha[i]] = {}

                    if sotoon == 'نام':
                        allData[namadha[i]][sotoon] = meqdar
                        continue
                    if sotoon not in allData[namadha[i]]:
                        allData[namadha[i]][sotoon] = []

                    allData[namadha[i]][sotoon].append(
                        {'v': meqdar, 'pd': pd, 'eInWeek': dayInWeek, 'pInWeek': pdayInWeek})
                    i += 1

            # print(pd)

    for namad in allData:
        for sotoon in allData[namad]:
            if sotoon == 'نام':
                continue
            allData[namad][sotoon].sort(key=lambda k: k['pd'])

    f = open(OutputFile, "wb")
    pickle.dump(allData, f)
    f.close()


# To merge daily xls files to python dictionary. Output is sorted interm of persian date
def mergeIranbourseAllDayExcelsByDays(InputDir="DailyExcelsFromIranBourse", OutputFile="AllDataByDays.pkl"):
    jdatetime.set_locale('fa_IR')

    allData = {}
    # if not os.path.exists(InputDir):
    #     os.makedirs(InputDir)

    for root, dirs, files in os.walk(InputDir):
        files.sort()
        print('start readin files')
        fi = 0.0
        for filename in files:
            print(str(int(fi / files.__len__() * 100.0)) + ' %  ... ' + filename)
            fi += 1.0
            try:
                df_list = pandas.read_html(InputDir + '/' + filename)
            except ValueError as e:
                if e.args[0] == 'No tables found':
                    continue
                else:
                    raise e

            if len(df_list) < 1:
                print('no Data Frame in > ' + filename)
                continue

            df = df_list[0]  # first frame only !
            # df.to_csv('DataPreparing/Data/table {}.csv'.format(0))
            if df.isnull().values.any():
                print('null value in > ' + filename)
                continue

            date = filename.split('.')[0].split('_')
            pd = jdatetime.date(int(date[1]), int(date[2]), int(date[3]))
            ed = pd.togregorian()
            dayInWeek = ed.strftime("%A")
            pdayInWeek = pd.strftime("%A")

            thisday = {}
            for col in df.columns.values:
                # thisday[col] = df[col].values
                idx = 0
                for v in df[col].values:
                    if idx not in thisday:
                        thisday[idx] = {}
                    thisday[idx][col] = v
                    idx += 1

            allData[pd] = thisday

    f = open(OutputFile, "wb")
    pickle.dump(allData, f)
    f.close()


# To merge daily xls files to python dictionary. Output is sorted interm of persian date
def mergeIranbourseAllNamadExcelsByNamadd(InputDir="NamadsExcelsFromIranBourse", OutputFile="AllDataByNamads.pkl"):
    jdatetime.set_locale('fa_IR')

    allData = {}

    for root, dirs, files in os.walk(InputDir):
        files.sort()
        print('start readin files')
        fi = 0.0
        for filename in files:
            print(str(int(fi / files.__len__() * 100.0)) + ' %  ... ' + filename)
            fi += 1.0
            try:
                df_list = pandas.read_html(InputDir + '/' + filename)
            except ValueError as e:
                if e.args[0] == 'No tables found':
                    continue
                else:
                    raise e

            if len(df_list) < 1:
                print('no Data Frame in > ' + filename)
                continue

            df = df_list[0]  # first frame only !
            # df.to_csv('DataPreparing/Data/table {}.csv'.format(0))
            if df.isnull().values.any():
                print('null value in > ' + filename)
                continue

            parts = filename.split('.')[0].split('_')
            NamadId = parts[1]
            NamadCode = parts[2]

            thisNamad = {}
            for col in df.columns.values:
                idx = 0
                for v in df[col].values:
                    if idx not in thisNamad:
                        thisNamad[idx] = {}
                    if col == str('تاريخ'):
                        date = v.split('/')
                        pd = jdatetime.date(int(date[0]), int(date[1]), int(date[2]))
                        thisNamad[idx][col] = pd
                    else:
                        if type(v) == numpy.int64:
                            thisNamad[idx][col] = int(v)
                        else:
                            thisNamad[idx][col] = v
                    idx += 1

            allData[NamadId] = thisNamad

    f = open(OutputFile, "wb")
    pickle.dump(allData, f)
    f.close()
