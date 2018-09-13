import datetime
import pickle

import numpy
from matplotlib import pyplot

from statsmodels.tsa.seasonal import seasonal_decompose

log = open('log.txt', 'w')

# load data
f = open("AllData.pkl", "rb")
allData = pickle.load(f)

print('start writing resaults for ' + str(allData.__len__()) + ' namad')

# allData[namad][sotoon].sort(key=lambda k: k['pd'])

AnalysisDataForAll = {}


def drawDataWithTrendLine(series, z, name):
    x = range(len(series))
    pyplot.plot(x, series, 'o')
    p = numpy.poly1d(z)
    pyplot.plot(range(len(series)), p(x),'r-')
    pyplot.suptitle(name)
    pyplot.show()


for namad in allData:
    print(namad)

    namadData = allData[namad]

    try:
        name = namadData['نام']
    except:
        namad = namad
    arzesh = namadData['ارزش']
    bishtarin = namadData['بیشترین']
    kamtarin = namadData['کمترین']
    hajm = namadData['حجم']
    dafaatmoamele = namadData['دفعات معامله']
    qeymatpayani = namadData['مقدار قیمت پایانی']
    taqirqeymatpayani = namadData['تغییر قیمت پایانی']
    darsadqeymatpayani = namadData['درصد قیمت پایانی']
    akharinqeymat = namadData['مقدار آخرین قیمت']
    taqirakharinqeymat = namadData['تغییر آخرین قیمت']
    darsadakharintaqir = namadData['درصد آخرین قیمت']
    qeymatroozqabl = namadData['قیمت روز قبل']
    arzeshbazar = namadData['ارزش بازار']

    AnalysisDataForAll[namad] = {}
    AnalysisDataForAll[namad]['tedad_roozhayee_ke_namad_tu_300ta_bude'] = bishtarin.__len__()

    dafaatseries = [int(d['v']) for d in dafaatmoamele]
    AnalysisDataForAll[namad]['miangeen_tedad_moamelat_dar_rooz_baraye_kolle_dadeha'] = sum(dafaatseries)/len(dafaatseries)
    z = numpy.polyfit(range(len(dafaatmoamele)), dafaatseries, 1)
    AnalysisDataForAll[namad]['dafaatTrendLine'] = z
    # drawDataWithTrendLine(dafaatseries, z, namad + '-' + 'dafaat moamele')


    bishtarinseries = [int(d['v']) for d in bishtarin]
    z = numpy.polyfit(range(len(bishtarin)), bishtarinseries, 1)
    AnalysisDataForAll[namad]['bishtarinTrendLine'] = z
    # drawDataWithTrendLine(bishtarinseries, z, namad + '-' + 'bishtarin')

    kamtarinseries = [int(d['v']) for d in kamtarin]
    z = numpy.polyfit(range(len(kamtarin)), kamtarinseries, 1)
    AnalysisDataForAll[namad]['kamtarinTrendLine'] = z
    # drawDataWithTrendLine(kamtarinseries, z, namad + '-' + 'kamtarin')

    kamtarinbishtarinfaseleseries = numpy.asarray(bishtarinseries) - numpy.asarray(kamtarinseries)
    z = numpy.polyfit(range(len(kamtarinbishtarinfaseleseries)), kamtarinbishtarinfaseleseries, 1)
    AnalysisDataForAll[namad]['kamtarinbishtarinfaseleTrendLine'] = z
    # drawDataWithTrendLine(kamtarinbishtarinfaseleseries, z, namad + '-' + 'kamtarin bishtarin fasele')





