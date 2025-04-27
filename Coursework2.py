import pandas as pd
from sklearn.preprocessing import MinMaxScaler

diet_df=pd.read_csv("Results_21Mar2022.csv")
metrics = ['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 'mean_bio', 'mean_watuse', 'mean_acid']

#Works out the weighted value for each metric
for metric in metrics:
     diet_df[f'{metric}_weighted']=diet_df[metric]*diet_df['n_participants']

weighted_metrics=[]
for metric in metrics:
    weighted_metrics.append(f'{metric}_weighted')

#groups the data and aggregates metric values 
aggregation={weighted_metric:'sum' for weighted_metric in weighted_metrics }
aggregation['n_participants']='sum'

ave_diet_df=diet_df.groupby(['diet_group','age_group']).agg(aggregation).reset_index()

#Calcuating the weighted average
for metric in metrics:
    ave_diet_df[metric]=ave_diet_df[f'{metric}_weighted']/ave_diet_df['n_participants']

#Normalisation of metrics
for metric in metrics:          
    ave_diet_df[metric]= (
    (ave_diet_df[metric]-ave_diet_df[metric].min()) /
    (ave_diet_df[metric].max()-ave_diet_df[metric].min()))

#Reshapes the data for radar charts
finished_diet_df=ave_diet_df.melt(id_vars=['age_group','diet_group'],value_vars=metrics,var_name='metric',value_name='value')


finished_diet_df.to_excel('Prepared_Diet_DataV3.xlsx')

