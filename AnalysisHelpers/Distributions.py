import math
import os
import pickle

import arabic_reshaper
import bidi.algorithm
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def computePercentOfChangeDistributionForAllNamadsAsWhole(OutputDir="Distiribution", InputFile="AllData.pkl"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    f = open(InputFile, "rb")
    allData = pickle.load(f)
    f.close()

    print('start writing resaults for ' + str(allData.__len__()) + ' day')

    GroupByMonth = {}
    for day in allData:
        DayData = allData[day]
        key = f'{day.year:02}' + '-' + f'{day.month:02}'
        if key not in GroupByMonth:
            GroupByMonth[key] = []

        for Namad in DayData:
            NamadData = DayData[Namad]

            try:
                Name = NamadData['نام']
            except KeyError:
                Name = day
            # Value = NamadData['ارزش']
            # Volume = NamadData['حجم']
            Maximum = NamadData['بیشترین']
            Minimum = NamadData['کمترین']
            ExchangeCount = NamadData['دفعات معامله']
            ClosePrice = NamadData['مقدار قیمت پایانی']
            # taqirqeymatpayani = DayData[
            #     'تغییر قیمت پایانی']  # «قیمت پایانی» برابر با میانگین وزنی قیمت‌های معامله‌شده در همان روز است.
            PercentOfClosePrice = NamadData['درصد قیمت پایانی']  # میانگین قیمت سهم در روز
            LastPrice = NamadData[
                'مقدار آخرین قیمت']  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
            # taqirakharinqeymat = NamadData['تغییر آخرین قیمت']
            PercentOfLastPrice = NamadData['درصد آخرین قیمت']  # آخرین قیمت معامله شده
            # PriceOfPreDay = NamadData['قیمت روز قبل']
            ValueOfBazzar = NamadData['ارزش بازار']  # ارزش کل سهام های نماد

            GroupByMonth[key].append(float(PercentOfClosePrice))

    HistOfMonth = {}
    for m in sorted(GroupByMonth.keys()):
        a = np.asarray(GroupByMonth[m])
        hist, bin_edges = np.histogram(a, density=True)
        # _counts = Counter(a)

        # plt.hist(a, bin_edges)
        # plt.suptitle(str(m))

        # plt.show()
        HistOfMonth[m] = {'hist': hist, 'bin': bin_edges, 'avg': np.average(a), 'median': np.median(a),
                          'mode': stats.mode(a)}

    f = open(OutputDir + '/PercentOfChangeDistributionForAllNamadsAsWhole.pkl', "wb")
    pickle.dump(allData, f)
    f.close()


def computePercentOfChangeDistributionForAllNamads(OutputDir="Distiribution", InputFile="AllNamadsByNamads.pkl"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    f = open(InputFile, "rb")
    allData = pickle.load(f)
    f.close()

    print('start writing resaults for ' + str(allData.__len__()) + ' Namad')

    pr = 0
    GroupByNamad = {}
    for Namad in allData:
        NamadData = allData[Namad]

        if Namad not in GroupByNamad:
            GroupByNamad[Namad] = []

        GroupByMonth = {}
        for val in NamadData:
            DayData = NamadData[val]
            day = DayData['تاريخ']
            key = f'{day.year:02}' + '-' + f'{day.month:02}'
            if key not in GroupByMonth:
                GroupByMonth[key] = []

            try:
                Name = DayData['نام']
            except KeyError:
                Name = Namad
            # Value = DayData['ارزش']
            # Volume = DayData['حجم']
            Maximum = DayData['بیشترین']
            Minimum = DayData['کمترین']
            ExchangeCount = DayData['دفعات معامله']
            ClosePrice = DayData['مقدار قیمت پایانی']
            # taqirqeymatpayani = DayData[
            #     'تغییر قیمت پایانی']  # «قیمت پایانی» برابر با میانگین وزنی قیمت‌های معامله‌شده در همان روز است.
            PercentOfClosePrice = DayData['درصد قیمت پایانی']  # میانگین قیمت سهم در روز
            LastPrice = DayData[
                'مقدار آخرین قیمت']  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
            # taqirakharinqeymat = DayData['تغییر آخرین قیمت']
            PercentOfLastPrice = DayData['درصد آخرین قیمت']  # آخرین قیمت معامله شده
            # PriceOfPreDay = DayData['قیمت روز قبل']
            ValueOfBazzar = DayData['ارزش بازار']  # ارزش کل سهام های نماد

            GroupByMonth[key].append(float(PercentOfClosePrice))

        HistOfMonth = {}
        for m in sorted(GroupByMonth.keys()):
            a = np.asarray(GroupByMonth[m])
            hist, bin_edges = np.histogram(a, density=True)
            # _counts = Counter(a)

            # plt.hist(a, 'auto)
            # reshaped_text = arabic_reshaper.reshape(Namad)
            # text = bidi.algorithm.get_display(reshaped_text)
            # plt.suptitle(text + ' > '+str(m))

            # plt.show()
            average = np.average(a)
            median = np.median(a)
            mode = stats.mode(a)
            std = np.std(a)
            HistOfMonth[m] = {'hist': hist, 'bin': bin_edges, 'avg': average, 'median': median, 'mode': mode,
                              'std': std}

        GroupByNamad[Namad] = HistOfMonth

    f = open(OutputDir + '/PercentOfChangeDistributionForAllNamads.pkl', "wb")
    pickle.dump(allData, f)
    f.close()
