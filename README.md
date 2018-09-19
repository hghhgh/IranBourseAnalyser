## Iran bourse data downloader and analyzer

Extract and Analys data from [Iran bourse or stock exchange](http://www.iranbourse.com/archive/)

دانلود و تحلیل کننده داده های بورس اوراق بهادار تهران

# Our preference in decision support and inference approach are as below :
1. **Bayesian Approach**, like :  _Bayesian Inference_
    - To prevent overfitting on small data
    - To use human expertise 
2. **Machine Learning** Technologies, like : _Neural network_
    - To handel time series with large input dimension
    - To use useful libraries
3. **Frequentist Inference**, such as : _hypothesis testing_ and other _data science_ techniques
    - To apply descriptive analysis
    - To apply diagnostic analysis
    - To apply prescriptive analysis
    - To apply predictive analysis


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

# and more ...

# for new function and their usage see "main.py" file

```

- AnalysisHelpers :
```python

```

- DecisionSupports :
```python

```


# Helps and Tutorial Articles

## Analysis useful links
1. Bayesian Inference
    - [Introduction to Bayesian Inference](https://www.datascience.com/blog/introduction-to-bayesian-inference-learn-data-science-tutorials)
    - [PyMC: Bayesian Stochastic Modelling in Python](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3097064/)
    - [BayesPy: Variational Bayesian Inference in Python](http://www.jmlr.org/papers/volume17/luttinen16a/luttinen16a.pdf)
    - [Frequentism and Bayesianism: A Python-driven Primer](https://arxiv.org/abs/1411.5018)
    - [Frequentism and Bayesianism: A Practical Introduction](https://jakevdp.github.io/blog/2014/03/11/frequentism-and-bayesianism-a-practical-intro/)
    - [Bayesian Statistics at Coursera](https://www.coursera.org/learn/bayesian/home/welcome)
2. 

## Data sets useful links
- [آموزش بورس اوراق بهادار](http://tse.ir/amuzesh.html)
- [انواع تحلیل](http://tse.ir/cms/Portals/1/Amouzesh/33-ravesh%20haye%20tahlilpdf.pdf)
- فیلم های آموزشی انواع تحلیل
    - [ویدیوهای تکنیکال مقدماتی](https://www.aparat.com/video/video/listuser/username/agahex/usercat/84240)
    - [ویدیوهای تکنیکال پیشرفته](https://www.aparat.com/video/video/listuser/username/agahex/usercat/83118)
    - [ویدیوهای تحلیل بنیادی مقدماتی](https://www.aparat.com/video/video/listuser/username/agahex/usercat/83486)
- [حجم مبنا و قیمت پایانی](https://files.ershants.ir/fileserver/source/1062/%d8%ad%d8%ac%d9%85%20%d9%85%d8%a8%d9%86%d8%a7/%d8%ad%d8%ac%d9%85_%d9%85%d8%a8%d9%86%d8%a7.pdf)

### Support or Contact

email me : hosein.ghiasy _at_ gmail.com