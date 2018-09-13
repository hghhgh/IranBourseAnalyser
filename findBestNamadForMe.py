# بهترین نماد چیست ؟
# اونی که ویٓژگی های زیر رو داشته باشه :
# 1. وجود داشته باشه زمانی که در طول دو هفته (یا یک ماه) که اگر بخری و بفروشی ۴ درصد سود کنی
# در طول این دو هفته مثلا هر روز به تعداد سهمی که باید سود کنه خرید و فروش بشه
# حجم خرید و فروش به حداکثر ۱۰۰ هزار تومن باشه
#
import datetime
import pickle

import jdatetime

log = open('log.txt', 'w')

# load data
f = open("AllData.pkl", "rb")
allData = pickle.load(f)

print('start writing resaults for ' + str(allData.__len__()) + ' namad')

for namad in allData:
    print(namad)

    namadData = allData[namad]

    name = namadData['نام']
    arzesh = namadData['ارزش']
    bishtarin = namadData['بیشترین']
    kamtarin = namadData['کمترین']
    hajm = namadData['حجم']
    dafaat = namadData['دفعات معامله']
    qeymatpayani = namadData['مقدار قیمت پایانی']
    taqirqeymatpayani = namadData['تغییر قیمت پایانی']
    darsadqeymatpayani = namadData['درصد قیمت پایانی']
    akharinqeymat = namadData['مقدار آخرین قیمت']
    taqirakharinqeymat = namadData['تغییر آخرین قیمت']
    darsadakharintaqir = namadData['درصد آخرین قیمت']

    size = bishtarin.__len__()

    for pnt1 in range(0, size):
        for pnt2 in range(pnt1, size):

            bish1 = bishtarin[pnt1]
            bish2 = bishtarin[pnt2]

            datBish1 = bish1['pd']
            datBish2 = bish2['pd']

            dtemp = jdatetime.date.today().togregorian()

            # within next n week : from 7 to 14 day later
            if datBish1.togregorian() + datetime.timedelta(7) < datBish2.togregorian():
                if datBish1.togregorian() + datetime.timedelta(14) > datBish2.togregorian():
                    vBish1 = bish1['v']
                    vBish2 = bish2['v']
                    if vBish2 > vBish1:
                        growth = vBish2 - vBish1
                        perc = (growth / vBish1) * 100
                        if perc > 1:
                            print('prophit detected !')
                            print('Buy on: ' + datBish1.isoformat())
                            print('Sell on: ' + datBish2.isoformat())
                            print(str(int(perc*100)/100) + ' %' )
                            print(growth)