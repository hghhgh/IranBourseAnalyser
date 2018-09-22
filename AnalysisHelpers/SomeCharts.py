import os
import pickle

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas
from bidi import algorithm as bidialg
import arabic_reshaper

# plt.style.use('fivethirtyeight')
# plt.style.use('ggplot')
# plt.style.use('seaborn-whitegrid')
matplotlib.rcParams["figure.figsize"] = (16, 10)
plt.rcParams['image.interpolation'] = 'nearest'


def drawScaters(OutputDir="Charts", InputFile="AllNamadsByNamads.pkl"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    f = open(InputFile, "rb")
    allData = pickle.load(f)
    f.close()

    print('start writing resaults for ' + str(allData.__len__()) + ' Namad')

    pr = 0
    for Namad in allData:
        NamadData = allData[Namad]

        # Value = DayData['ارزش']
        # Volume = DayData['حجم']
        Maximum = [NamadData[DayData]['بیشترین'] for DayData in NamadData]
        Minimum = [NamadData[DayData]['کمترین'] for DayData in NamadData]
        ExchangeCount = [NamadData[DayData]['دفعات معامله'] for DayData in NamadData]
        ClosePrice = [NamadData[DayData]['مقدار قیمت پایانی'] for DayData in NamadData]
        # taqirqeymatpayani = DayData[
        #     'تغییر قیمت پایانی']  # «قیمت پایانی» برابر با میانگین وزنی قیمت‌های معامله‌شده در همان روز است.
        PercentOfClosePrice = [NamadData[DayData]['درصد قیمت پایانی'] for DayData in
                               NamadData]  # میانگین قیمت سهم در روز
        LastPrice = [NamadData[DayData][
                         'مقدار آخرین قیمت'] for DayData in
                     NamadData]  # «قیمت آخرین معامله» برابر است با آخرین قیمتی که تا آن لحظه معامله شده است.
        # taqirakharinqeymat = DayData['تغییر آخرین قیمت']
        PercentOfLastPrice = [NamadData[DayData]['درصد آخرین قیمت'] for DayData in NamadData]  # آخرین قیمت معامله شده
        # PriceOfPreDay = [DayData['قیمت روز قبل'] for DayData in NamadData]
        ValueOfBazzar = [NamadData[DayData]['ارزش بازار'] for DayData in NamadData]  # ارزش کل سهام های نماد

        plt.clf()
        # 1th Figure
        plt.subplot(221)
        x = (np.asarray(PercentOfClosePrice))
        y = (np.asarray(ExchangeCount))
        try:
            # Linear Regression
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
            # Scatter
            plt.scatter(x, y)
            plt.xlabel('PercentOfClosePrice')
            plt.ylabel('ExchangeCount')
        except:
            pass

        # 2th Figure
        plt.subplot(222)
        x = np.log(np.asarray(ValueOfBazzar) + 1)
        y = (np.asarray(ExchangeCount))
        try:
            # Linear Regression
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
            # Scatter
            plt.scatter(x, y)
            plt.xlabel('log ValueOfBazzar')
            plt.ylabel('ExchangeCount')
        except:
            pass

        # 3th Figure
        plt.subplot(223)
        x = (np.asarray(PercentOfLastPrice))
        y = np.log(np.asarray(ValueOfBazzar) + 1)
        try:
            # Linear Regression
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
            # Scatter
            plt.scatter(x, y)
            plt.xlabel('PercentOfLastPrice')
            plt.ylabel('log ValueOfBazzar')
        except:
            pass

        # 4th Figure
        plt.subplot(224)
        x = (np.asarray(PercentOfLastPrice))
        y = (np.asarray(PercentOfLastPrice))
        try:
            # Linear Regression
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
            # Scatter
            plt.scatter(x, y)
            plt.xlabel('PercentOfLastPrice')
            plt.ylabel('PercentOfLastPrice')
        except:
            pass

        reshaped_text = arabic_reshaper.reshape(Namad)
        text = bidialg.get_display(reshaped_text)
        plt.suptitle(text)
        plt.savefig(OutputDir + '/' + '_' + Namad + '_' + '.png')
        # plt.show()
        pr += 1
        print(Namad + ' > ' + str(int(pr / len(allData) * 100)) + ' % done!')


def drawCorrelations(InputDir='NamadsExcelsFromIranBourse', OutputDir="Charts/IntraNamadCorrelations"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    allData = {}

    fig = plt.figure()

    for root, dirs, files in os.walk(InputDir):
        files.sort()
        print('start readin files')
        fi = 0
        for filename in files:
            print(str(int(fi / files.__len__() * 100.0)) + ' %  ... ' + filename)
            fi += 1.0
            df_list = pandas.read_html(InputDir + '/' + filename)

            if len(df_list) < 1:
                print('no Data Frame in > ' + filename)
                continue

            df = df_list[0]  # first frame only !
            # df.to_csv('DataPreparing/Data/table {}.csv'.format(0))
            if df.isnull().values.any():
                print('null value in > ' + filename)
                continue

            parts = filename.split('.')[0].split('_')
            NamadId = parts[1]
            NamadCode = parts[2]

            thisNamadCorr = df.corr()

            allData[NamadId] = thisNamadCorr

            fig.clf()
            ax = fig.add_subplot(111)
            cax = ax.matshow(thisNamadCorr, cmap='coolwarm', vmin=-1, vmax=1)
            fig.colorbar(cax)
            ticks = np.arange(0, len(thisNamadCorr.columns), 1)
            ax.set_xticks(ticks)
            plt.xticks(rotation=90)
            ax.set_yticks(ticks)
            xl = [bidialg.get_display(arabic_reshaper.reshape(tx)) for tx in thisNamadCorr.columns]
            ax.set_xticklabels(xl)
            ax.set_yticklabels(xl)
            reshaped_text = arabic_reshaper.reshape(NamadId)
            text = bidialg.get_display(reshaped_text)
            plt.suptitle(text, y=.08)
            plt.savefig(OutputDir + '/' + NamadCode + '_' + NamadId + '_' + '.png')
            # plt.show()
