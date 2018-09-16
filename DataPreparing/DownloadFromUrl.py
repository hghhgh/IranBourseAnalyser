import codecs
from urllib.parse import unquote
import requests
import jdatetime
import datetime
import os

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# Automatic downloading of daily bourse data as .xls file
def downloadAllDayExcelsFromIranbourse(OutDir='excels'):
    if not os.path.exists(OutDir):
        os.makedirs(OutDir)

    numberOfDayIgnore = 10  # check : not data available on the server
    numberOfFileIgnore = 10  # check : data existed on local system
    # example = 'http://www.iranbourse.com/archive/Trade/Cash/TradeOneDay/TradeOneDay_1396_2_18.xls'
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


# download namad data. the name of namad will be extracted from @param Inputfile
def downloadAllNamadExcelsFromIranbourse(OutputDir='NamadsExcelsFromIranBourse'):
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    Namads = []
    # extract indicesHTMLFile eith ids
    # save this url ( 'http://new.tse.ir/indices.html') using browser and then use it
    f = codecs.open('Data/indicesHTMLFile/بورس اوراق بهادار تهران - نمودار شاخص ها.html', encoding='utf-8')
    htmltxt = f.read()
    f.close()
    parsed_html = BeautifulSoup(htmltxt, 'lxml')
    for idc in parsed_html.find_all('td'):
        if 'title' in idc.attrs and 'id' in idc.attrs:
            title = idc.attrs['title']
            id = idc.attrs['id']
            Namads.append({'title': title, 'id': id})

    # another list from
    # save this url ( 'http://tse.ir/listing.html?section=alphabet&cat=cash') using browser and then use it
    f = codecs.open('Data/indicesHTMLFile/بورس اوراق بهادار تهران - لیست شرکت ها.html', encoding='utf-8')
    htmltxt = f.read()
    f.close()
    parsed_html = BeautifulSoup(htmltxt, 'lxml')
    for idc in parsed_html.find_all('a'):
        if 'href' in idc.attrs:
            ad = idc.attrs['href']
            if '/instrument/' in ad:
                par = ad.split('/')[4].split('.')[0].split('_')
                id = par[1]
                title = unquote(par[0])
                Namads.append({'title': title, 'id': id})

    # example : http://www.iranbourse.com/archive/Trade/Cash/SymbolTrade/SymbolTrade_IRO1BHMN0002.xls
    bourseSite = 'http://www.iranbourse.com/archive/Trade/Cash/SymbolTrade/'
    fn = 0
    for namad in Namads:
        filename = 'SymbolTrade_' + namad['title'] + '_' + namad['id'] + '_.xls'

        # check if the file existed or not
        if os.path.exists(OutputDir + '/' + filename):
            print('file : `' + filename + '` already exists !. ')
            continue

        # go for next file to download
        url = bourseSite + 'SymbolTrade_' + namad['id'] + '.xls'
        r = requests.get(url)

        # check if the file downloaded correctly
        if r.status_code == 200:
            # open method to open a file on your system and write the contents
            with open(OutputDir + '/' + filename, "wb") as code:
                code.write(r.content)
        else:
            print('Cannot get file : ' + filename + ' !. ')

        fn += 1
        print(str(int(fn / len(Namads) * 100.)) + '% > ' + namad['title'])
