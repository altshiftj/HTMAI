import pandas as pd
import matplotlib.pyplot as plt
import os

path_L23_active =   'C:\Environments\HTMAI\Code\Output\L23_Active'
path_L4_active =    'C:\Environments\HTMAI\Code\Output\L4_Active'
path_L6a_active =    'C:\Environments\HTMAI\Code\Output\L6a_Active'

L23_exist = os.path.exists(path_L23_active)
L4_exist = os.path.exists(path_L4_active)
L6a_exist = os.path.exists(path_L6a_active)

if not L23_exist:
    os.makedirs(path_L23_active)

if not L4_exist:
    os.makedirs(path_L4_active)

if not L6a_exist:
    os.makedirs(path_L6a_active)

df = pd.read_csv("C:\Environments\HTMAI\Code\cell_fire.csv")

selected_columns = ['layer', 'thought_count', 'cell', 'column', 'x', 'y', 'head_direction','linear_speed','angular_velocity']

df_1, df_2, df_3 = [x for _, x in df.groupby(df['layer'])]

for i in range(256):
    j=i*32
    if not df_1.loc[df_1['cell'] == j].empty:
        df_1.loc[(df_1['cell'] == j)].to_csv(f'C:\Environments\HTMAI\Code\Output\L23_Active\cell{j}.csv')

for i in range(256):
    j = i * 32
    if not df_2.loc[df_2['cell'] == j].empty:
        df_2.loc[(df_2['cell'] == j)].to_csv(f'C:\Environments\HTMAI\Code\Output\L4_Active\cell{j}.csv')

for i in range(256):
    j = i * 32
    if not df_3.loc[df_3['cell'] == j].empty:
        df_3.loc[(df_3['cell'] == j)].to_csv(f'C:\Environments\HTMAI\Code\Output\L6a_Active\cell{j}.csv')