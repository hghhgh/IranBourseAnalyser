## Iran bourse data downloader and analyzer

Extract and Analys data from [Iran bourse or stock exchange](http://www.iranbourse.com/archive/)

دانلود و تحلیل کننده داده های بورس اوراق بهادار تهران

### Files and their descriptions

# This project has 3 packages 

1. DataPrepairing
2. AnalysisHelpers
3. DecisionSupports

The last package is the main one !


## with following usage examples :

- DataPrepairing : 
```python
from DataPreparing import DownloadFromUrl
from DataPreparing import MergeFiles
from DataPreparing import ExtractNewDataFilesFromAnother
from DataPreparing import MakeGroupOfData

# Update Downloaded Data
DownloadFromUrl.downloadAllDayExcelsFromIranbourse(OutDir='Data/excels')
print('raw data updated !')

# Merge Iranbourse daily excel to python dict pkl file
MergeFiles.mergeIranbourseAllDayExcels(InputDir='Data/excels', OutputFile="Data/AllData.pkl")
print('all xls merged !')

# To use .pkl file created in step 2 and create .xls per Namad
ExtractNewDataFilesFromAnother.createXLSforNamadFromPkl(OutputDir='Data/namads', InputFile='Data/AllData.pkl')
print('XLS for each namad has been created !')

# Make Group of Data for each Namad in term of the day of a week : like شنبه یا یکشنبه
MakeGroupOfData.groupNamadDataIntermOfDayOfWeekFromPKL(InputFile='Data/AllData.pkl', OutputDir='Data/namadsOnDayOfWeek')
print('Data were grouped by the day of the week. ')
```

- AnalysisHelpers :
```python

```

- DecisionSupports :
```python

```


# Helps and Tutorial Articles

- [آموزش بورس اوراق بهادار](http://tse.ir/amuzesh.html)
- [انواع تحلیل](http://tse.ir/cms/Portals/1/Amouzesh/33-ravesh%20haye%20tahlilpdf.pdf)
- فیلم های آموزشی انواع تحلیل
    - [ویدیوهای تکنیکال مقدماتی](https://www.aparat.com/video/video/listuser/username/agahex/usercat/84240)
    - [ویدیوهای تکنیکال پیشرفته](https://www.aparat.com/video/video/listuser/username/agahex/usercat/83118)
    - [ویدیوهای تحلیل بنیادی مقدماتی](https://www.aparat.com/video/video/listuser/username/agahex/usercat/83486)
- [حجم مبنا و قیمت پایانی](https://files.ershants.ir/fileserver/source/1062/%d8%ad%d8%ac%d9%85%20%d9%85%d8%a8%d9%86%d8%a7/%d8%ad%d8%ac%d9%85_%d9%85%d8%a8%d9%86%d8%a7.pdf)

### Support or Contact

email me : hosein.ghiasy _at_ gmail.com