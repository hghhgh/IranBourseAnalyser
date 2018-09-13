import datetime
import pickle

import numpy
import matplotlib
from matplotlib import pyplot

from statsmodels.tsa.seasonal import seasonal_decompose

# matplotlib.rc('font', family='Arial')

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
    # pyplot.suptitle(name)
    pyplot.title(name)  # .encode('utf-8'))
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
    taqirqeymatpayani = namadData[
        'تغییر قیمت پایانی']  # «قیمت پایانی» برابر با میانگین وزنی قیمت‌های معامله‌شده در همان روز است.
    darsadqeymatpayani = namadData['درصد قیمت پایانی']  # میانگین قیمت سهم در روز
    akharinqeymat = namadData[
        'مقدار آخرین قیمت']  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
    taqirakharinqeymat = namadData['تغییر آخرین قیمت']
    darsadakharintaqir = namadData['درصد آخرین قیمت']  # آخرین قیمت معامله شده
    qeymatroozqabl = namadData['قیمت روز قبل']
    arzeshbazar = namadData['ارزش بازار']

    # extract scores :
    AnalysisDataForAll[namad] = {}
    AnalysisDataForAll[namad]['tedad_roozhayee_ke_namad_tu_300ta_bude'] = bishtarin.__len__()

    dafaatseries = [int(d['v']) for d in dafaatmoamele]
    AnalysisDataForAll[namad]['miangeen_tedad_moamelat_dar_rooz_baraye_kolle_dadeha'] = sum(dafaatseries)/len(dafaatseries)
    z = numpy.polyfit(range(len(dafaatmoamele)), dafaatseries, 1)
    AnalysisDataForAll[namad]['dafaatTrendLine'] = z
    drawDataWithTrendLine(dafaatseries, z, namad + '-' + 'dafaat moamele')

    darsadqeymatpayaniseries = [float(d['v']) for d in darsadqeymatpayani]
    z = numpy.polyfit(range(len(darsadqeymatpayani)), darsadqeymatpayaniseries, 1)
    AnalysisDataForAll[namad]['bishtarinTrendLine'] = z
    drawDataWithTrendLine(darsadqeymatpayaniseries, z, namad + '-' + 'darsad qeymat payani')

    darsadakharintaqirseries = [float(d['v']) for d in darsadakharintaqir]
    z = numpy.polyfit(range(len(darsadakharintaqir)), darsadakharintaqirseries, 1)
    AnalysisDataForAll[namad]['kamtarinTrendLine'] = z
    drawDataWithTrendLine(darsadakharintaqirseries, z, namad + '-' + 'darsad akharin taqir')

    kamtarinbishtarinfaseleseries = numpy.asarray([float(d['v']) for d in bishtarin]) - numpy.asarray(
        [float(d['v']) for d in kamtarin])
    z = numpy.polyfit(range(len(kamtarinbishtarinfaseleseries)), kamtarinbishtarinfaseleseries, 1)
    AnalysisDataForAll[namad]['kamtarinbishtarinfaseleTrendLine'] = z
    drawDataWithTrendLine(kamtarinbishtarinfaseleseries, z, namad + '-' + 'kamtarin bishtarin fasele')
