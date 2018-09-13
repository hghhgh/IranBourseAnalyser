import random

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.testing import *
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import keras
import os

log = open('log.txt', 'w')

# load data
maindir = 'namadsOnDayOfWeek'

if not os.path.exists(maindir):
    os.makedirs(maindir)

# filename = 'خبهمن1.xls'
filename = 'ولساپا1.xls'
rawdata = pd.ExcelFile(maindir + '/' + filename)
for sh in rawdata.sheet_names:
    print(sh)
    log.write(sh + '\n')
    roozHafte = rawdata.parse(sh)

    # prepare data
    size = int(roozHafte.shape[0])
    try:
        arzesh = roozHafte['ارزش'].astype(np.int)
        bishtarin = roozHafte['بیشترین'].astype(np.int)
        kamtarin = roozHafte['کمترین'].astype(np.int)
        hajm = roozHafte['حجم'].astype(np.int)
        dafaat = roozHafte['دفعات معامله'].astype(np.int)
        qeymatpayani = roozHafte['مقدار قیمت پایانی'].astype(np.int)
        taqirqeymatpayani = roozHafte['تغییر قیمت پایانی'].astype(np.int)
        darsadqeymatpayani = roozHafte['درصد قیمت پایانی'].astype(np.int)
        akharinqeymat = roozHafte['مقدار آخرین قیمت'].astype(np.int)
        taqirakharinqeymat = roozHafte['تغییر آخرین قیمت'].astype(np.int)
        darsadakharintaqir = roozHafte['درصد آخرین قیمت'].astype(np.int)
    except:
        continue

    tarikh = roozHafte['تاریخ']

    inputduration = 4
    datasetlen = size - inputduration
    inputs = []
    targets = []

    windowsize = (inputduration + 1)
    for i in range(0, int(datasetlen / windowsize)):
        sample = np.zeros((inputduration, 11))
        for j in range(0, inputduration):
            sample[j, 0] = arzesh[i * windowsize + j]
            sample[j, 1] = bishtarin[i * windowsize + j]
            sample[j, 2] = kamtarin[i * windowsize + j]
            sample[j, 3] = hajm[i * windowsize + j]
            sample[j, 4] = dafaat[i * windowsize + j]
            sample[j, 5] = qeymatpayani[i * windowsize + j]
            sample[j, 6] = taqirqeymatpayani[i * windowsize + j]
            sample[j, 7] = darsadqeymatpayani[i * windowsize + j]
            sample[j, 8] = akharinqeymat[i * windowsize + j]
            sample[j, 9] = taqirakharinqeymat[i * windowsize + j]
            sample[j, 10] = darsadakharintaqir[i * windowsize + j]

        inputs.append(sample)


        tar = np.zeros((1, 11))
        tar[0, 0] = arzesh[i * windowsize + inputduration]
        tar[0, 1] = bishtarin[i * windowsize + inputduration]
        tar[0, 2] = kamtarin[i * windowsize + inputduration]
        tar[0, 3] = hajm[i * windowsize + inputduration]
        tar[0, 4] = dafaat[i * windowsize + inputduration]
        tar[0, 5] = qeymatpayani[i * windowsize + inputduration]
        tar[0, 6] = taqirqeymatpayani[i * windowsize + inputduration]
        tar[0, 7] = darsadqeymatpayani[i * windowsize + inputduration]
        tar[0, 8] = akharinqeymat[i * windowsize + inputduration]
        tar[0, 9] = taqirakharinqeymat[i * windowsize + inputduration]
        tar[0, 10] = darsadakharintaqir[i * windowsize + inputduration]

        targets.append(tar)

    X = np.asarray(inputs)
    Y = np.asarray(targets)

    # random permutation
    # rpi = [i for i in range(X.shape[0])]
    # random.shuffle(rpi)
    #
    # X = X[rpi,:,:]
    # Y = Y[rpi,:,:]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, shuffle=True, test_size=.2, random_state=2)

    # to 2D
    X_train2D = X_train.reshape((X_train.shape[0], X_train.shape[1] * X_train.shape[2]))
    Y_train2D = Y_train.reshape((Y_train.shape[0], Y_train.shape[1] * Y_train.shape[2]))
    X_test2D = X_test.reshape((X_test.shape[0], X_test.shape[1] * X_test.shape[2]))
    Y_test2D = Y_test.reshape((Y_test.shape[0], Y_test.shape[1] * Y_test.shape[2]))

    # standardize
    scalerX = StandardScaler()
    scalerX.fit(X_train2D)
    StandardScaler(copy=True, with_mean=True, with_std=True)
    # Now apply the transformations to the data:
    X_train2D = scalerX.transform(X_train2D)
    X_test2D = scalerX.transform(X_test2D)

    scalerY = StandardScaler()
    scalerY.fit(Y_train2D)
    StandardScaler(copy=True, with_mean=True, with_std=True)
    # Now apply the transformations to the data:
    Y_train2D = scalerY.transform(Y_train2D)
    Y_test2D = scalerY.transform(Y_test2D)

    # restor size and data
    X_train = X_train2D.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2]))
    X_test = X_test2D.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2]))
    Y_train = Y_train2D.reshape((Y_train.shape[0], Y_train.shape[1], Y_train.shape[2]))
    Y_test = Y_test2D.reshape((Y_test.shape[0], Y_test.shape[1], Y_test.shape[2]))

    # learn a model
    bestr = 99999
    bestm = []
    besths = 0
    randomHiddenSizes = []
    for xt in range(10):
        randomHiddenSizes.append([random.randint(23, 33), random.randint(23, 33)])

    for hs in randomHiddenSizes:
        print('**********1 = {Dense} <keras.layers.core.Dense object at 0x7f9365471748>*************************************************************************** hs: ' + str(hs))
        model = keras.models.Sequential()
        # model.add(keras.layers.Convolution2D(3, 3, 3, activation='tanh', input_shape=(X_train.shape[1], X_train.shape[2], 1)))
        # model.add(keras.layers.Convolution2D(4, 3, 3, activation='tanh', input_shape=(X_train.shape[1]-2, X_train.shape[2]-2, 1)))
        # model.add(keras.layers.Convolution2D(5, 3, 3, activation='tanh', input_shape=(X_train.shape[1]-4, X_train.shape[2]-4, 1)))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(units=hs[0], activation='tanh'))
        model.add(keras.layers.Dense(units=hs[1], activation='tanh'))
        model.add(keras.layers.Dense(units=Y_train2D.shape[1], use_bias=False))
        model.compile(loss='mean_squared_error',
                      optimizer=keras.optimizers.SGD(lr=0.13, momentum=0.95, nesterov=True))
        model.fit(X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1), Y_train2D, epochs=1000)
        loss_and_metrics = model.evaluate(X_test.reshape(X_test.shape[0],X_test.shape[1],X_test.shape[2],1), Y_test2D)

        # show the results

        # print(loss_and_metrics)
        # print(classes)
        if loss_and_metrics < bestr:
            bestr = loss_and_metrics
            bestm = model
            besths = hs

            print(str(hs)+' : '+str(bestr))
            log.write(str(hs)+' : '+str(bestr) + '\n')

    print('final > ')
    print(str(hs) + ' : ' + str(bestr))
    log.write(str(hs) + ' : ' + str(bestr))
    log.flush()

    fig = plt.figure()
    fig.suptitle(sh)
    predte = bestm.predict(X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1))
    predtr = bestm.predict(X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1))
    maxtest = fig.add_subplot(221)
    maxtrain = fig.add_subplot(222)
    mintest = fig.add_subplot(223)
    mintrain = fig.add_subplot(224)

    maxtest.set_title('maximum value test')
    maxtest.scatter(Y_test[1], predte[1], s=1, c='r', marker="s", label='real')
    xmax = Y_test[1].max()
    xmin = Y_test[1].min()
    maxtest.add_line(mlines.Line2D([xmin, xmax], [xmin, xmax], color='b'))

    maxtrain.set_title('maximum value train')
    maxtrain.scatter(Y_train[1], predtr[1], s=1, c='r', marker="s", label='real')
    xmax = Y_train[1].max()
    xmin = Y_train[1].min()
    maxtrain.add_line(mlines.Line2D([xmin, xmax], [xmin, xmax], color='b'))


    mintest.set_title('minimum value test')
    mintest.scatter(Y_test[2], predte[2], s=1, c='r', marker="s", label='real')
    xmax = Y_test[2].max()
    xmin = Y_test[2].min()
    mintest.add_line(mlines.Line2D([xmin, xmax], [xmin, xmax], color='b'))

    mintrain.set_title('minimum value train')
    mintrain.scatter(Y_train[2], predtr[2], s=1, c='r', marker="s", label='real')
    xmax = Y_train[2].max()
    xmin = Y_train[2].min()
    mintrain.add_line(mlines.Line2D([xmin, xmax], [xmin, xmax], color='b'))
    # mintrain.scatter(Y_train[2],Y_train[2], s=1, c='b', marker="s", label='real')

    fig.savefig('trainAmodelResults/'+sh+'.png')
    plt.show()
    # break

plt.show()
log.close()