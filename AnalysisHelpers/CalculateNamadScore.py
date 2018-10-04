# from __future__ import unicode_literals

import datetime
import math
import pickle

import arabic_reshaper
import bidi.algorithm
import numpy
from matplotlib import pyplot

# install font on ubuntu using : sudo apt-get install msttcorefonts
# matplotlib.font_manager._rebuild()
from AnalysisHelpers.Helpers import MutualInformation
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
    reshaped_text = arabic_reshaper.reshape(name)
    text = bidi.algorithm.get_display(reshaped_text)
    pyplot.title(text)
    pyplot.show()


def findBestDelayBetweenBuyAndSell(Dates, ClosePrice, LastPrice, minDays, maxDays):
    # ! warning : input arrays should be sorted interm of dates

    # Profits = []
    ProfitsOnLengths = {}
    for buy in range(0, len(ClosePrice) - maxDays):
        if math.isnan(ClosePrice[buy]):
            continue
        buydate = Dates[buy]
        for sell in range(minDays, maxDays):
            if math.isnan(ClosePrice[buy + sell]):
                continue
            selldate = Dates[buy + sell]
            if selldate > buydate + datetime.timedelta(
                    maxDays):  # some days may be holyday and dont have data in the array
                break

            ProfitPrice, ProfitPercent = getSingleNamadProfitValue(Dates, ClosePrice, LastPrice, buy, sell)
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


def calculateScores(InputFile="AllNamadsByNamads.pkl", MinDataLen=100, OutputDir=""):
    # load data
    f = open(InputFile, "rb")
    Data = pickle.load(f)
    f.close()

    adsize = Data.__len__()
    print('start writing scores for ' + str(adsize) + ' namad')

    AnalysisDataResult = {}
    nidx = 0
    for Namad in Data:
        AnalysisDataResult[Namad] = {}
        NamadData = Data[Namad]

        Dates = [NamadData[k]['تاريخ'] for k in NamadData]
        MinMaxDistanceSeries = numpy.asarray([NamadData[k]['بیشترین'] for k in NamadData]) - numpy.asarray(
            [NamadData[k]['کمترین'] for k in NamadData])
        ExchangeCount = [NamadData[k]['دفعات معامله'] for k in NamadData]
        ClosePrice = [NamadData[k]['مقدار قیمت پایانی'] for k in NamadData]
        # taqirqeymatpayani = NamadData[
        #     'تغییر قیمت پایانی']  # «قیمت پایانی» برابر با میانگین وزنی قیمت‌های معامله‌شده در همان روز است.
        PercentOfClosePrice = [NamadData[k]['درصد قیمت پایانی'] for k in NamadData]  # میانگین قیمت سهم در روز
        LastPrice = [NamadData[k]['مقدار آخرین قیمت'] for k in
                     NamadData]  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
        # taqirakharinqeymat = [NamadData[k]['تغییر آخرین قیمت'] for k in NamadData]
        PercentOfLastPrice = [NamadData[k]['درصد آخرین قیمت'] for k in NamadData]  # آخرین قیمت معامله شده
        PriceOfPreDay = [NamadData[k]['قیمت روز قبل'] for k in NamadData]
        ValueOfBazzar = [NamadData[k]['ارزش بازار'] for k in NamadData]  # ارزش کل سهام های نماد

        # atleast MinDataLen data needed
        if len(ClosePrice) < MinDataLen:
            print('Small data : ' + str(len(ClosePrice)) + ' > ' + Namad)
            continue

        CurrentAnalysis = {}
        # extract scores :
        CurrentAnalysis['tedad_roozhayee_ke_namad_tu_300ta_bude'] = len(NamadData)

        z = numpy.polyfit(range(len(ValueOfBazzar)), ValueOfBazzar, 1)
        CurrentAnalysis['ValueOfBazzarTrendLine'] = z
        # drawDataWithTrendLine(ValueOfBazzar, z, Namad + '-' + 'ارزش بازار کل سهام های نماد')

        CurrentAnalysis['miangeen_tedad_moamelat_dar_rooz_baraye_kolle_dadeha'] = sum(ExchangeCount) / len(
            ExchangeCount)
        z = numpy.polyfit(range(len(ExchangeCount)), ExchangeCount, 1)
        CurrentAnalysis['dafaatTrendLine'] = z
        # drawDataWithTrendLine(ExchangeCount, z, Namad + '-' + 'دفعات معامله')

        z = numpy.polyfit(range(len(PercentOfClosePrice)), PercentOfClosePrice, 1)
        CurrentAnalysis['bishtarinTrendLine'] = z
        # drawDataWithTrendLine(PercentOfClosePrice, z, Namad + '-' + 'درصد قیمت پایانی')

        z = numpy.polyfit(range(len(PercentOfLastPrice)), PercentOfLastPrice, 1)
        CurrentAnalysis['kamtarinTrendLine'] = z
        # drawDataWithTrendLine(PercentOfLastPrice, z, Namad + '-' + 'درصد آخرین قیمت')

        z = numpy.polyfit(range(len(MinMaxDistanceSeries)), MinMaxDistanceSeries, 1)
        CurrentAnalysis['kamtarinbishtarinfaseleTrendLine'] = z
        # drawDataWithTrendLine(MinMaxDistanceSeries, z, Namad + '-' + 'فاصله بیشترین و کمترین قیمت')

        BestExpectedDelay, ExpectedProfitPrice, ExpectedProfitPercent = findBestDelayBetweenBuyAndSell(Dates,
                                                                                                       ClosePrice,
                                                                                                       LastPrice, 7, 27)
        CurrentAnalysis['BestDelayBetweenBuyAndSell'] = {'BestExpectedDelay': BestExpectedDelay,
                                                                   'ExpectedProfitPrice': ExpectedProfitPrice,
                                                                   'ExpectedProfitPercent': ExpectedProfitPercent}

        # Lower entropy means more predictable random variable
        entpp, normentpp = MutualInformation.computeEntropy4Continuous(PercentOfClosePrice, per=1)
        CurrentAnalysis['entropy_price_percent'] = normentpp

        # ppmi = metrics.mutual_info_score([round(p, 2) for p in PercentOfClosePrice[0:-BestExpectedDelay]],
        #                                  [round(p, 2) for p in PercentOfClosePrice[BestExpectedDelay:]])
        # nppmi = metrics.normalized_mutual_info_score([round(p, 2) for p in PercentOfClosePrice[0:-BestExpectedDelay]],
        #                                              [round(p, 2) for p in PercentOfClosePrice[BestExpectedDelay:]])
        ppmi, nppmi = MutualInformation.computMutualInformation4Continuous(PercentOfClosePrice[0:-BestExpectedDelay],
                                                                           PercentOfClosePrice[BestExpectedDelay:],
                                                                           per=1)
        CurrentAnalysis['mutual_info_price_percent_and_price_percent_with_best_expected_delay'] = nppmi

        entp, normentp = MutualInformation.computeEntropy4Discrete(ClosePrice)
        CurrentAnalysis['entropy_price'] = normentp

        entex, normentex = MutualInformation.computeEntropy4Discrete(ExchangeCount)
        CurrentAnalysis['entropy_exchange'] = normentex

        # filter very bad Namads !
        # if
        AnalysisDataResult[Namad] = CurrentAnalysis

        nidx += 1
        print(str(int(nidx / adsize * 100)) + '% done > ' + Namad)

    # save results
    f = open(OutputDir + "/NamadScores.pkl", "wb")
    pickle.dump(AnalysisDataResult, f)
    f.close()
