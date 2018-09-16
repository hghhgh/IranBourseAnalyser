import jdatetime
import pandas
import os
import pickle


# To merge daily xls files to python dictionary. Output is sorted interm of persian date
def mergeIranbourseAllDayExcels(InputDir="excels", OutputFile="AllData.pkl"):
    jdatetime.set_locale('fa_IR')

    allData = {}
    if not os.path.exists(InputDir):
        os.makedirs(InputDir)

    for root, dirs, files in os.walk(InputDir):
        files.sort()
        print('start readin files')
        fi = 0.0
        for filename in files:
            print(str(int(fi / files.__len__() * 100.0)) + ' %  ... ' + filename)
            fi += 1.0
            df_list = pandas.read_html(InputDir + '/' + filename)

            if len(df_list) < 1:
                print('no Data Frame in > ' + filename)
                continue

            df = df_list[0]  # first frame only !
            # df.to_csv('Data/table {}.csv'.format(0))
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
