# from __future__ import unicode_literals

import datetime
import math
import pickle
from bidi import algorithm as bidialg
import numpy
from matplotlib import pyplot

# import matplotlib

# install font on ubuntu using : sudo apt-get install msttcorefonts
# matplotlib.font_manager._rebuild()
from AnalysisHelpers.Profit import *

pyplot.rc('font', family='Arial')  # Arial, Thahoma, Times New Roman
# pyplot.style.use('fivethirtyeight')
pyplot.style.use('ggplot')


def drawDataWithTrendLine(series, z, name):
    x = range(len(series))
    pyplot.plot(x, series, 'o')
    p = numpy.poly1d(z)
    pyplot.plot(range(len(series)), p(x), 'r-')
    # pyplot.suptitle(name)
    text = bidialg.get_display(name)  # .encode('utf-8'))
    pyplot.title(text)
    pyplot.show()


def findBestDelayBetweenBuyAndSell(Maximum, Minimum, ClosePrice, LastPrice, minDays, maxDays):
    # ! warning : input arrays should be sorted interm of dates

    # Profits = []
    ProfitsOnLengths = {}
    for buy in range(0, len(ClosePrice) - maxDays):
        if math.isnan(ClosePrice[buy]['v']):
            continue
        buydate = ClosePrice[buy]['pd']
        for sell in range(minDays, maxDays):
            if math.isnan(ClosePrice[buy + sell]['v']):
                continue
            selldate = ClosePrice[buy + sell]['pd']
            if selldate > buydate + datetime.timedelta(
                    maxDays):  # some days may be holyday and dont have data in the array
                break

            ProfitPrice, ProfitPercent = getProfitValue(Maximum, Minimum, ClosePrice, LastPrice, buy, sell)
            SellDelay = (selldate - buydate).days
            # Profits.append(
            #     {'ProfitPrice': ProfitPrice, 'ProfitPercent': ProfitPercent,
            #      'SellDelay': SellDelay, 'Buy': buydate, 'Sell': selldate})
            if SellDelay not in ProfitsOnLengths:
                ProfitsOnLengths[SellDelay] = []
            ProfitsOnLengths[SellDelay].append({'ProfitPrice': ProfitPrice, 'ProfitPercent': ProfitPercent})

    # Profits.sort(key=lambda k: k['ProfitPercent'], reverse=True)

    ProfitsOnLengthsPercentMeans = []  # mean of profits -> E[Profit=n|delay=m]
    for dl in ProfitsOnLengths:
        m = 0
        mpri = 0
        for v in ProfitsOnLengths[dl]:
            m += v['ProfitPercent']
            mpri += v['ProfitPrice']
        m /= len(ProfitsOnLengths[dl])
        mpri /= len(ProfitsOnLengths[dl])
        ProfitsOnLengthsPercentMeans.append({'DelayDays': dl, 'Mean': m, 'MeanPrice': mpri})
    ProfitsOnLengthsPercentMeans.sort(key=lambda k: k['Mean'], reverse=True)

    # # following values are good but not useful now. we use previouse ones
    # ProfitsOnLengthsGroupByPercent = {} # conditional probability of P(Profit=n|delay=m)
    # ProfitExpectedValueInPercent = [] # conditional expectation E[Profit=n|delay=m]
    # for v in ProfitsOnLengths :
    #     ProfitsOnLengthsGroupByPercent[v] = []
    #     plen = len(ProfitsOnLengths[v])
    #     for k, g in itertools.groupby(ProfitsOnLengths[v], lambda x: x['ProfitPercent']):
    #         lg = list(g)
    #         # ProfitsOnLengthsGroupByPercent[v].append({'list':lg, 'percent':k, 'prob':len(lg)/plen})
    #         ProfitsOnLengthsGroupByPercent[v].append({'percent':k, 'prob':len(lg)/plen})
    #     ProfitsOnLengthsGroupByPercent[v].sort(key=lambda k: k['prob'], reverse=True)
    #     ev = 0
    #     for pp in ProfitsOnLengthsGroupByPercent[v]:
    #         ev += pp['percent']*pp['prob']
    #     ProfitExpectedValueInPercent.append({'delay':v, 'ev':ev})
    # ProfitExpectedValueInPercent.sort(key=lambda k: k['ev'], reverse=True)

    if len(ProfitsOnLengthsPercentMeans) > 0:
        BestExpectedDelay = ProfitsOnLengthsPercentMeans[0]['DelayDays']
        ExpectedProfitPrice = float(ProfitsOnLengthsPercentMeans[0]['MeanPrice'])
        ExpectedProfitPercent = float(ProfitsOnLengthsPercentMeans[0]['Mean'])

        return BestExpectedDelay, ExpectedProfitPrice, ExpectedProfitPercent
    else:
        return -1, -1, -1


def calculateScors(Data, MinDataLen):
    adsize = Data.__len__()
    print('start writing scores for ' + str(adsize) + ' namad')

    AnalysisDataResult = {}
    nidx = 0
    for Namad in Data:
        AnalysisDataResult[Namad] = {}
        NamadData = Data[Namad]

        try:
            Name = NamadData['نام']
        except KeyError:
            Name = Namad
        # Value = NamadData['ارزش']
        # Volume = NamadData['حجم']
        Maximum = NamadData['بیشترین']
        Minimum = NamadData['کمترین']
        ExchangeCount = NamadData['دفعات معامله']
        ClosePrice = NamadData['مقدار قیمت پایانی']
        # taqirqeymatpayani = NamadData[
        #     'تغییر قیمت پایانی']  # «قیمت پایانی» برابر با میانگین وزنی قیمت‌های معامله‌شده در همان روز است.
        PercentOfClosePrice = NamadData['درصد قیمت پایانی']  # میانگین قیمت سهم در روز
        LastPrice = NamadData[
            'مقدار آخرین قیمت']  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
        # taqirakharinqeymat = NamadData['تغییر آخرین قیمت']
        PercentOfLastPrice = NamadData['درصد آخرین قیمت']  # آخرین قیمت معامله شده
        # PriceOfPreDay = NamadData['قیمت روز قبل']
        ValueOfBazzar = NamadData['ارزش بازار']  # ارزش کل سهام های نماد

        # atleast MinDataLen data needed
        if len(ClosePrice) < MinDataLen:
            print('Small data : ' + str(len(ClosePrice)) + ' > ' + Namad)
            continue

        # extract scores :
        AnalysisDataResult[Namad][Name] = Name
        AnalysisDataResult[Namad]['tedad_roozhayee_ke_namad_tu_300ta_bude'] = Maximum.__len__()

        ValueOfBazzarSeries = [float(d['v']) for d in ValueOfBazzar]
        z = numpy.polyfit(range(len(ValueOfBazzar)), ValueOfBazzarSeries, 1)
        AnalysisDataResult[Namad]['ValueOfBazzarTrendLine'] = z
        # drawDataWithTrendLine(ValueOfBazzarSeries, z, Namad + '-' + 'ارزش بازار کل سهام های نماد')

        ExchangeCountSeries = [int(d['v']) for d in ExchangeCount]
        AnalysisDataResult[Namad]['miangeen_tedad_moamelat_dar_rooz_baraye_kolle_dadeha'] = sum(
            ExchangeCountSeries) / len(
            ExchangeCountSeries)
        z = numpy.polyfit(range(len(ExchangeCount)), ExchangeCountSeries, 1)
        AnalysisDataResult[Namad]['dafaatTrendLine'] = z
        # drawDataWithTrendLine(ExchangeCountSeries, z, Namad + '-' + 'دفعات معامله')

        PercentOfClosePriceSeries = [float(d['v']) for d in PercentOfClosePrice]
        z = numpy.polyfit(range(len(PercentOfClosePrice)), PercentOfClosePriceSeries, 1)
        AnalysisDataResult[Namad]['bishtarinTrendLine'] = z
        # drawDataWithTrendLine(PercentOfClosePriceSeries, z, Namad + '-' + 'درصد قیمت پایانی')

        PercentOfLastPriceSeries = [float(d['v']) for d in PercentOfLastPrice]
        z = numpy.polyfit(range(len(PercentOfLastPrice)), PercentOfLastPriceSeries, 1)
        AnalysisDataResult[Namad]['kamtarinTrendLine'] = z
        # drawDataWithTrendLine(PercentOfLastPriceSeries, z, Namad + '-' + 'درصد آخرین قیمت')

        MinMaxDistanceSeries = numpy.asarray([float(d['v']) for d in Maximum]) - numpy.asarray(
            [float(d['v']) for d in Minimum])
        z = numpy.polyfit(range(len(MinMaxDistanceSeries)), MinMaxDistanceSeries, 1)
        AnalysisDataResult[Namad]['kamtarinbishtarinfaseleTrendLine'] = z
        # drawDataWithTrendLine(MinMaxDistanceSeries, z, Namad + '-' + 'فاصله بیشترین و کمترین قیمت')

        BestExpectedDelay, ExpectedProfitPrice, ExpectedProfitPercent = findBestDelayBetweenBuyAndSell(Maximum, Minimum,
                                                                                                       ClosePrice,
                                                                                                       LastPrice, 7, 27)
        AnalysisDataResult[Namad]['BestDelayBetweenBuyAndSell'] = {'BestExpectedDelay': BestExpectedDelay,
                                                                   'ExpectedProfitPrice': ExpectedProfitPrice,
                                                                   'ExpectedProfitPercent': ExpectedProfitPercent}

        nidx += 1
        print(str(int(nidx / adsize * 100)) + '% done > ' + Namad)

    return AnalysisDataResult


# run main function
# load data
f = open("AllData.pkl", "rb")
AllData = pickle.load(f)
f.close()

AnalysisDataForAll = calculateScors(AllData, 100)

# save results
f = open("NamadScores.pkl", "wb")
pickle.dump(AnalysisDataForAll, f)
f.close()
