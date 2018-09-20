import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas

plt.rc('font', family='Arial')  # Arial, Thahoma, Times New Roman


# plt.style.use('fivethirtyeight')
# plt.style.use('ggplot')


def drawScaters(OutputDir="Charts", InputFile="AllNamadsByNamads.pkl"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    f = open(InputFile, "rb")
    allData = pickle.load(f)
    f.close()

    print('start writing resaults for ' + str(allData.__len__()) + ' Namad')

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

        # 1th Figure
        plt.subplot(221)
        x = (np.asarray(PercentOfClosePrice))
        y = (np.asarray(ExchangeCount))
        # Linear Regression
        try:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
        except:
            pass
        # Scatter
        plt.scatter(x, y)
        plt.xlabel('PercentOfClosePrice')
        plt.ylabel('ExchangeCount')

        # 2th Figure
        plt.subplot(222)
        x = np.log(np.asarray(ValueOfBazzar) + 1)
        y = (np.asarray(ExchangeCount))
        # Linear Regression
        try:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
        except:
            pass
        # Scatter
        plt.scatter(x, y)
        plt.xlabel('log ValueOfBazzar')
        plt.ylabel('ExchangeCount')

        # 3th Figure
        plt.subplot(223)
        x = (np.asarray(PercentOfLastPrice))
        y = np.log(np.asarray(ValueOfBazzar) + 1)
        # Linear Regression
        try:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
        except:
            pass
        # Scatter
        plt.scatter(x, y)
        plt.xlabel('PercentOfLastPrice')
        plt.ylabel('log ValueOfBazzar')

        # 4th Figure
        plt.subplot(224)
        x = (np.asarray(PercentOfLastPrice))
        y = (np.asarray(PercentOfLastPrice))
        # Linear Regression
        try:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), 'r-')
        except:
            pass
        # Scatter
        plt.scatter(x, y)
        plt.xlabel('PercentOfLastPrice')
        plt.ylabel('PercentOfLastPrice')

        plt.suptitle(Namad)
        plt.show()


def drawCorrelations(InputDir='NamadsExcelsFromIranBourse', OutputDir="Charts/IntraNamadCorrelations"):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    allData = {}

    for root, dirs, files in os.walk(InputDir):
        files.sort()
        print('start readin files')
        fi = 0.0
        for filename in files:
            print(str(int(fi / files.__len__() * 100.0)) + ' %  ... ' + filename)
            fi += 1.0
            df_list = pandas.read_html(InputDir + '/' + filename)

            if len(df_list) < 1:
                print('no Data Frame in > ' + filename)
                continue

            df = df_list[0]  # first frame only !
            # df.to_csv('Data/table {}.csv'.format(0))
            if df.isnull().values.any():
                print('null value in > ' + filename)
                continue

            parts = filename.split('.')[0].split('_')
            NamadId = parts[1]
            NamadCode = parts[1]

            thisNamadCorr = df.corr()

            allData[NamadId] = thisNamadCorr

            fig = plt.figure()
            ax = fig.add_subplot(111)
            cax = ax.matshow(thisNamadCorr, cmap='coolwarm', vmin=-1, vmax=1)
            fig.colorbar(cax)
            ticks = np.arange(0, len(df.columns), 1)
            ax.set_xticks(ticks)
            plt.xticks(rotation=90)
            ax.set_yticks(ticks)
            ax.set_xticklabels(df.columns)
            ax.set_yticklabels(df.columns)
            plt.savefig(OutputDir + '/' + NamadId + '_' + NamadCode + '.png')
            plt.show()
