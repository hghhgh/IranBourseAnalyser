# import DataPreparing.PrepareAllData
# DataPreparing.PrepareAllData.DownloadAll()
# DataPreparing.PrepareAllData.MergeAll()
# DataPreparing.PrepareAllData.ExtractAll()

# import AnalysisHelpers.Distributions
# AnalysisHelpers.Distributions.computePercentOfChangeDistributionForAllNamadsAsWhole(InputFile='DataPreparing/Data/AllDataByDays.pkl', OutputDir='AnalysisHelpers/Distributions')
# AnalysisHelpers.Distributions.computePercentOfChangeDistributionForAllNamads(InputFile='DataPreparing/Data/AllNamadsByNamads.pkl', OutputDir='AnalysisHelpers/Distributions')

# import AnalysisHelpers.SomeCharts
# AnalysisHelpers.SomeCharts.drawScaters(InputFile='DataPreparing/Data/AllNamadsByNamads.pkl', OutputDir='AnalysisHelpers/SomeCharts/Scatters')
# AnalysisHelpers.SomeCharts.drawCorrelations(InputDir='DataPreparing/Data/NamadsExcelsFromIranBourse', OutputDir="AnalysisHelpers/SomeCharts/IntraNamadCorrelations")

import AnalysisHelpers.CalculateNamadScore
AnalysisHelpers.CalculateNamadScore.calculateScors(InputFile='DataPreparing/Data/AllNamadsByNamads.pkl', MinDataLen=100,
                                                   OutputDir="AnalysisHelpers/Scores")
