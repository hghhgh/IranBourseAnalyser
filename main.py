from DataPreparing import DownloadFromUrl
from DataPreparing import MergeFiles
from DataPreparing import ExtractNewDataFilesFromAnother
from DataPreparing import MakeGroupOfData

# # Update Downloaded Data
# DownloadFromUrl.downloadAllDayExcelsFromIranbourse(OutDir='Data/excels')
# print('raw data updated !')
#
# Merge Iranbourse daily excel to python dict pkl file
MergeFiles.mergeIranbourseAllDayExcels(InputDir='Data/excels', OutputFile="Data/AllData.pkl")
print('all xls merged !')
#
# # To use .pkl file created in step 2 and create .xls per Namad
# ExtractNewDataFilesFromAnother.createXLSforNamadFromPkl(OutputDir='Data/namads', InputFile='Data/AllData.pkl')
# print('XLS for each namad has been created !')
#
# # Make Group of Data for each Namad in term of the day of a week : like شنبه یا یکشنبه
# MakeGroupOfData.groupNamadDataIntermOfDayOfWeekFromPKL(InputFile='Data/AllData.pkl', OutputDir='Data/namadsOnDayOfWeek')
# print('Data were grouped by the day of the week. ')


# DownloadFromUrl.downloadAllNamadExcelsFromIranbourse(OutputDir='Data/NamadsExcelsFromIranBourse')
