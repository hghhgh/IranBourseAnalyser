import requests
import jdatetime
import datetime
import os.path

numberOfDayIgnor = 10 # for not data available
#example = 'http://www.iranbourse.com/archive/Trade/Cash/TradeOneDay/TradeOneDay_1396_2_18.xls'
boorsSite = 'http://www.iranbourse.com/archive/Trade/Cash/TradeOneDay/'


ed = datetime.date.today() -  datetime.timedelta(2)
pd = jdatetime.date.fromgregorian(date=ed)
name = 'TradeOneDay_' + str(pd.year) + '_' + str(pd.month) + '_' + str(pd.day) + '.xls'

while os.path.exists('excels/'+name):
    ed = ed - datetime.timedelta(1)
    pd = jdatetime.date.fromgregorian(date=ed)
    name = 'TradeOneDay_' + str(pd.year) + '_' + str(pd.month) + '_' + str(pd.day) + '.xls'

url = boorsSite + name
r = requests.get(url)

nodata = 0
while nodata < numberOfDayIgnor:
    if r.status_code == 200:
        nodata = 0
        # open method to open a file on your system and write the contents
        with open('excels/'+name, "wb") as code:
            code.write(r.content)
    else:
        nodata += 1
        print(nodata)

    while os.path.exists('excels/' + name):
        ed = ed - datetime.timedelta(1)
        pd = jdatetime.date.fromgregorian(date=ed)
        name = 'TradeOneDay_' + str(pd.year) + '_' + str(pd.month) + '_' + str(pd.day) + '.xls'

    url = boorsSite + name
    # download the url contents in binary format
    r = requests.get(url)

