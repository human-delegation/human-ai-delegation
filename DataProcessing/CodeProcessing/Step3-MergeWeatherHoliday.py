import pandas as pd
import numpy as np
import os

file_list=os.listdir('../1-KPIsummary')
file_list.sort()

file1=pd.read_csv('../OtherInputs/WeeklyWeather_summary.csv')
allfiles=[]
for file in file_list:
    if '.csv' in file:
        store_id=int(file.split('.')[0])
        inputfile=pd.read_csv('../1-KPIsummary/'+str(store_id)+'.csv')
        allfiles.append(inputfile)
        allfiles_total=pd.concat(allfiles)

allfiles_total.replace([np.inf, -np.inf], np.nan, inplace=True)
allfiles_total.dropna(inplace=True)
averaged=allfiles_total.groupby('date').mean()

averaged_sales=averaged[['sale_improvement','sale_bakery_improvement','sale_dairy_improvement','sale_price10_improvement','sale_price20_improvement']]
averaged_sales=averaged_sales.rename(columns={'sale_improvement': "sale_improvement_average",'sale_bakery_improvement': "sale_bakery_improvement_average", "sale_dairy_improvement": "sale_dairy_improvement_average",
                                              "sale_price10_improvement":"sale_price10_improvement_average","sale_price20_improvement":"sale_price20_improvement_average"})

file_list=os.listdir('../1-KPIsummary/')
file_list.sort()

allfiles=[]
for file in file_list:
    if '.csv' in file:
        store_id=int(file.split('.')[0])
        file2=pd.read_csv('../1-KPIsummary/'+str(store_id)+'.csv')
        inputfile=pd.merge(file2, file1, how="left", on="date")
        inputfile=pd.merge(inputfile,averaged_sales,how="left",on="date")
        inputfile['outperform_area'] = inputfile['sale_improvement'] - inputfile['sale_improvement_average']
        inputfile['outperform_area_bakery']=inputfile['sale_bakery_improvement']-inputfile['sale_bakery_improvement_average']
        inputfile['outperform_area_dairy']=inputfile['sale_dairy_improvement']-inputfile['sale_dairy_improvement_average']
        inputfile['outperform_area_price10']=inputfile['sale_price10_improvement']-inputfile['sale_price10_improvement_average']
        inputfile['outperform_area_price20']=inputfile['sale_price20_improvement']-inputfile['sale_price20_improvement_average']
        inputfile.to_csv('../2-KPI-summary-with-weather/'+str(store_id)+'.csv', index = False)