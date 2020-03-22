from DataPreparing import DownloadFromUrl
from DataPreparing import MergeFiles
from DataPreparing import ExtractNewDataFilesFromAnother


def DownloadAll():
    # Update Downloaded Data
    DownloadFromUrl.downloadOverallDataExcelFromIranbourse(
        OutputDir='DataPreparing/Data/OverallDataExcelFromIranBourse')
    print('General index data downloaded !')

    # Update Downloaded Data
    DownloadFromUrl.downloadAllDayExcelsFromIranbourse(OutDir='DataPreparing/Data/DailyExcelsFromIranBourse')
    print('All day data downloaded !')

    # Update Downloaded Data
    DownloadFromUrl.downloadAllNamadExcelsFromIranbourse(OutputDir='DataPreparing/Data/NamadsExcelsFromIranBourse')


def MergeAll():
    # Merge Iranbourse daily excel to python dict pkl file
    MergeFiles.mergeIranbourseAllDayExcelsByNamads(InputDir='DataPreparing/Data/DailyExcelsFromIranBourse',
                                                   OutputFile="DataPreparing/Data/AllDataByNamad.pkl")
    print('all xls merged !')

    # Merge Iranbourse daily excel to python dict pkl file
    MergeFiles.mergeIranbourseAllDayExcelsByDays(InputDir='DataPreparing/Data/DailyExcelsFromIranBourse',
                                                 OutputFile="DataPreparing/Data/AllDataByDays.pkl")
    print('all xls merged !')

    # Merge Iranbourse namads excel to python dict pkl file
    MergeFiles.mergeIranbourseAllNamadExcelsByNamadd(InputDir='DataPreparing/Data/NamadsExcelsFromIranBourse',
                                                     OutputFile="DataPreparing/Data/AllNamadsByNamads.pkl")
    print('all xls merged !')


def ExtractAll():
    # To use .pkl file created in step 2 and create .xls per Namad
    ExtractNewDataFilesFromAnother.createXLSforNamadFromPkl(InputFile='DataPreparing/Data/AllData.pkl',
                                                            OutputDir='DataPreparing/Data/DailyExcelsFromIranBourse/Namads')
    print('XLS for each namad has been created !')

    # Make Group of Data for each Namad in term of the day of a week : like شنبه یا یکشنبه
    ExtractNewDataFilesFromAnother.groupNamadDataIntermOfDayOfWeekFromPKL(InputFile='DataPreparing/Data/AllData.pkl',
                                                                          OutputDir='DataPreparing/Data/DailyExcelsFromIranBourse/NamadsOnDayOfWeek')
    print('Data were grouped by the day of the week. ')
