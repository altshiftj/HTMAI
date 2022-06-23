from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from pylab import *
import pandas

layer = 'L4'

df = pandas.read_csv(f'C:\Environments\HTMAI\Code\cell_fire.csv')

#for i in range(450000, 600000)


select_df = df[(df['layer'] == layer)
            &  (df['thought count'] > 500000) & (df['thought count'] < 505000)
            &  (df['cell'] == 3488)]

# select_df = df[(df['layer'] == layer)
#             &  (df['cell'] == 100)
#             &  (df['cell'] == 100)]

select_df.to_csv('select_cells.csv')