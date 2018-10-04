# Combinations or Permutations
# Functions in this file will be used to produce conditional probabilities !
import datetime
import math
import pickle

import numpy

from AnalysisHelpers.Profit import getSingleNamadProfitValue

'''
co-occurrence of these random variables :
PerPro = Percent of profit
TDbBS = Time dealy between buy and sell
Bag = Custom combination of namads > bag of shares
Season = season based of date
TrendOfSeason = trend of profit is + or - of data group by season
Month = of date
TrendOfMonth = trend of profit is + or - of data group by month
TypeOfGov = eslahtalab or osulgara
NumOfGov = number of goverment 1, 2 ... , 11 , ...
TypeOfUSAGov = democrat or republican
GIdxBource = Grows Of Index Of Bource 
'''


def extractCombinations(InputFile="AllNamadsByNamads.pkl", MinDataLen=100, OutputDir=""):
    # load data
    f = open(InputFile, "rb")
    Data = pickle.load(f)
    f.close()

    adsize = len(Data)
    print('start writing scores for ' + str(adsize) + ' namad')

    PosibilitiesResult = {}
    nidx = 0
    for Namad in Data:
        NamadData = Data[Namad]
        if len(NamadData) < MinDataLen:
            continue

        PosibilitiesResult[Namad] = {}

        Dates = [NamadData[k]['تاريخ'] for k in NamadData]
        ClosePrice = [NamadData[k]['مقدار قیمت پایانی'] for k in NamadData]
        LastPrice = [NamadData[k]['مقدار آخرین قیمت'] for k in
                     NamadData]  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
        minDays = 7
        maxDays = 27

        TrendInMonths, GBDoWtrend, TrendInSeasons, GBYtrend = getTrendGroupBySomethingOverAllEntries(NamadData)

        ProfitsOnLengthsWithOtherData = {}
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
                if SellDelay not in ProfitsOnLengthsWithOtherData:
                    ProfitsOnLengthsWithOtherData[SellDelay] = []

                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Wrong maybe
                ProfitsOnLengthsWithOtherData[SellDelay].append({
                    'BuyDate': buydate,
                    'ProfitPrice': ProfitPrice,
                    'ProfitPercent': ProfitPercent,
                    'SeasonOfBuy': getSeason(buydate.month),
                    'TrendInSeasons': TrendInSeasons[getSeason(buydate.month)],
                    'MonthOfBuy': buydate.month,
                    'TrendInMonths': TrendInMonths[buydate.strftime("%B")],
                    # 'TypeOfGovOnBuy': TypeOfGovOnBuy,
                    # 'NumOfGovOnBuy': NumOfGovOnBuy,
                    # 'TypeOfUSAGovOnBuy': TypeOfUSAGov,
                    # 'GIdxBourceOnBuy': GIdxBourceOnBuy
                })

        nidx += 1
        print(str(int(nidx / adsize * 100)) + '% done > ' + Namad)

    # save results
    f = open(OutputDir + "/NamadEnumeratedData.pkl", "wb")
    pickle.dump(ProfitsOnLengthsWithOtherData, f)
    f.close()


def getTrendGroupBySomethingOverAllEntries(NamadData):
    GroupByMonth = {}
    GroupByDayOfWeek = {}
    GroupBySeason = {}
    GroupByYear = {}
    for k in NamadData:
        Date = NamadData[k]['تاريخ']

        key = Date.strftime("%B")
        if key not in GroupByMonth:
            GroupByMonth[key] = []
        GroupByMonth[key].append(NamadData[k])

        key = Date.strftime("%A")
        if key not in GroupByDayOfWeek:
            GroupByDayOfWeek[key] = []
        GroupByDayOfWeek[key].append(NamadData[k])

        key = getSeason(Date.month)
        if key not in GroupBySeason:
            GroupBySeason[key] = []
        GroupBySeason[key].append(NamadData[k])

        key = Date.year
        if key not in GroupByYear:
            GroupByYear[key] = []
        GroupByYear[key].append(NamadData[k])

    # GBMtrend = {}
    # for k in GroupByMonth:
    #     GBMtrend[k] = numpy.polyfit(range(len(GroupByMonth[k])),[v['مقدار قیمت پایانی'] for v in GroupByMonth[k]], 1)

    GBMtrend = {mon: numpy.polyfit(range(len(GroupByMonth[mon])),
                                   [v['مقدار قیمت پایانی'] for v in GroupByMonth[mon]], 1) for
                mon in GroupByMonth}
    GBDoWtrend = {mon: numpy.polyfit(range(len(GroupByDayOfWeek[mon])),
                                     [v['مقدار قیمت پایانی'] for v in GroupByDayOfWeek[mon]], 1) for
                  mon in GroupByDayOfWeek}
    GBStrend = {mon: numpy.polyfit(range(len(GroupBySeason[mon])),
                                   [v['مقدار قیمت پایانی'] for v in GroupBySeason[mon]], 1) for mon in
                GroupBySeason}
    GBYtrend = {mon: numpy.polyfit(range(len(GroupByYear[mon])),
                                   [v['مقدار قیمت پایانی'] for v in GroupByYear[mon]], 1) for mon in
                GroupByYear}

    return GBMtrend, GBDoWtrend, GBStrend, GBYtrend


def getSeason(month):
    # return (month%12 + 3)//3

    # if (month == "DECEMBER" or month == "JANUARY" or month == "FEBRUARY" or month == "MARCH"):
    #    return "WINTER"
    # elif(month == "APRIL" or month == "MAY"):
    #    return "SPRING"
    # elif(month =="JUNE" or month=="JULY" or month == "AUGUST" or month == "SEPTEMBER"):
    #    return "SUMMER"
    # else:
    #    return "FALL"
    # according to persian callender
    if month >= 10:
        return "WINTER"
    elif month <= 3:
        return "SPRING"
    elif 4 <= month <= 6:
        return "SUMMER"
    else:
        return "FALL"
