import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("cell_fire.csv")


selected_columns = ['thought_count', 'cell', 'column', 'x', 'y', 'head_direction']

for i in range(256*32):
    globals()['df_column_%s' %i] = df[df['cell'] == i]
    globals()['df_column_%s' %i].to_csv(f'C:\Environments\HTMAI\Output\cell{i}.csv')
