## Iran bourse data downloader and analyzer

Extract and Analys data from [Iran Bourse](http://www.iranbourse.com/archive/)

### Files and their descriptions

# Steps of using files
1. Automatic downloading of **daily** bourse data as .xls file : 
- `saveExcelFromUrl.py`
2. To merge daily _xls_ files to python dictionary :
- `mergExcelFiles.py`
3. To use .pkl file created in step 2 and create .xls per Namad :
- `convertPKLtoXLS.py`
4. To score each Namad in order to find the bests for buy:
- `calculateNamadScore.py`


### Support or Contact

email me : hosein.ghiasy _at_ gmail.com