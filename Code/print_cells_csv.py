import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("C:\Environments\HTMAI\Code\cell_fire.csv")

selected_columns = ['layer', 'thought_count', 'cell', 'column', 'x', 'y', 'head_direction','linear_speed','angular_velocity']

df_1, df_2 = [x for _, x in df.groupby(df['layer'])]

for i in range(256):
    j=i*32
    df_1.loc[df_1['cell'] == j].to_csv(f'C:\Environments\HTMAI\Code\Output\L4_Active\column{i}_cell{j}.csv')

# for i in range(256):
#     j=i*32
#     df_2.loc[df_2['cell'] == j].to_csv(f'C:\Environments\HTMAI\Code\Output\L4_Predictive\column{i}_cell{j}.csv')

for i in range(256):
    j = i * 32
    df_2.loc[df_2['cell'] == j].to_csv(f'C:\Environments\HTMAI\Code\Output\L6a_Active\column{i}_cell{j}.csv')

# for i in range(256):
#     j = i * 32
#     df_4.loc[df_4['cell'] == j].to_csv(f'C:\Environments\HTMAI\Code\Output\L6a_Predictive\column{i}_cell{j}.csv')
