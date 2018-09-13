import requests
import jdatetime
import datetime
import os

OutDir = 'excels'
if not os.path.exists(OutDir):
    os.makedirs(OutDir)

numberOfDayIgnore = 10  # check : not data available on the server
numberOfFileIgnore = 10  # check : data existed on local system
#example = 'http://www.iranbourse.com/archive/Trade/Cash/TradeOneDay/TradeOneDay_1396_2_18.xls'
bourseSite = 'http://www.iranbourse.com/archive/Trade/Cash/TradeOneDay/'
ed = datetime.date.today()

nodata = 0  # no data on the server
redata = 0  # repeated data
while nodata < numberOfDayIgnore and redata < numberOfFileIgnore:
    ed = ed - datetime.timedelta(1)
    pd = jdatetime.date.fromgregorian(date=ed)
    name = 'TradeOneDay_' + str(pd.year) + '_' + str(pd.month) + '_' + str(pd.day) + '.xls'

    # check if the file existed or not
    if os.path.exists(OutDir + '/' + name):
        redata += 1
        print('file :' + name + ' already exists !. repeated data = ' + str(redata))
        continue
    else:
        redata = 0

    # go for next file to download
    url = bourseSite + name
    # download the url contents in binary format
    r = requests.get(url)

    # check if the file downloaded correctly
    if r.status_code == 200:
        nodata = 0
        # open method to open a file on your system and write the contents
        with open(OutDir + '/' + name, "wb") as code:
            code.write(r.content)
    else:
        nodata += 1
        print('Cannot get file : ' + name + ' !. no data = ' + str(nodata))
