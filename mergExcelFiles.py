import jdatetime
import pandas
import os
import pickle


jdatetime.set_locale('fa_IR')

allData = {}
dir = "excels"
if not os.path.exists(dir):
    os.makedirs(dir)

for root, dirs, files in os.walk(dir):
    files.sort()
    print('start readin files')
    fi = 0.0
    for filename in files:
        print(str(int(fi/files.__len__()*100.0))+' %  ... ' + filename)
        fi += 1.0
        df_list = pandas.read_html(dir + '/' + filename)

        for i, df in enumerate(df_list):
            # print(df)
            df.to_csv('table {}.csv'.format(i))

        date = filename.split('.')[0].split('_')
        pd = jdatetime.date(int(date[1]), int(date[2]), int(date[3]))
        ed = pd.togregorian()
        dayInWeek = ed.strftime("%A")
        pdayInWeek = pd.strftime("%A")

        namadha = df['نماد'].values
        for sotoon in df.dtypes.index.values:
            # if t == 'نام' or t == 'نماد' :
            if sotoon == 'نماد' :
                continue
            # n =df[t].values
            i=0
            for meqdar in df[sotoon].values:
                if namadha[i] not in allData:
                    allData[namadha[i]] = {}

                if sotoon == 'نام' :
                    allData[namadha[i]][sotoon]=meqdar
                    continue
                if sotoon not in allData[namadha[i]]:
                    allData[namadha[i]][sotoon]=[]

                allData[namadha[i]][sotoon].append({'v': meqdar, 'pd':pd, 'eInWeek':dayInWeek, 'pInWeek':pdayInWeek})
                i += 1

        # print(pd)

for namad in allData:
    for sotoon in allData[namad]:
        if sotoon == 'نام':
            continue
        allData[namad][sotoon].sort(key=lambda k: k['pd'])

f = open("AllData.pkl","wb")
pickle.dump(allData,f)
f.close()
