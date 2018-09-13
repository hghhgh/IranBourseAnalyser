import os
import pickle
import xlwt

f = open("AllData.pkl", "rb")
allData = pickle.load(f)

print('start writing resaults for ' + str(allData.__len__()) + ' namad')

pr = 0
for namad in allData:

    if os.path.exists('namads/'+namad+'.xls'):
        continue

    book = xlwt.Workbook()

    namadPage = book.add_sheet(namad)
    c =0
    for sotoon in allData[namad]:
        if sotoon == 'نام' :
            continue

        # allData[namad][sotoon].sort(key=lambda k: k['pd'])
        namadPage.write(0, c+2, sotoon)

        vals = allData[namad][sotoon]
        r = 1
        for v in vals:
            namadPage.write(r, c, v['pInWeek'])
            namadPage.write(r, c + 1, v['pd'].isoformat())
            # namadPage.write(r, c + 1, v['pd'])
            try:
                namadPage.write(r, c+2, int(v['v']))
            except:
                namadPage.write(r, c+2, '-')

            r += 1

        c += 3

    pr += 1
    print(str(int(pr/allData.__len__()*100)) + '% ... namad: ' + namad + ' saved!')
    # if pr >10 :
    #     break

    book.save('namads/'+namad+'.xls')
