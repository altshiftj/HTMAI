import pandas as pd
import matplotlib.pyplot as plt
import os

def print_cells_csv():
    layers = [
        'L23',
        'L4',
        'L5a',
        'L5b',
        'L6a',
        'L6b'
    ]

    cell_type = 'active'

    read_path = "C:\Environments\HTMAI\Code\cell_fire.csv"

    df = pd.read_csv(read_path)

    selected_columns = ['layer', 'thought_count', 'cell', 'column', 'x', 'y', 'head_direction','linear_speed','angular_velocity']

    for l in range(len(layers)):
        write_path =   f'C:\Environments\HTMAI Output\\{layers[l]}_{cell_type}'
        path_exists = os.path.exists(write_path)

        if not path_exists:
            os.makedirs(write_path)

        layer_data = df.loc[df['layer'] == f'{layers[l]}_{cell_type}']

        for i in range(256):
            j = i * 32
            if not layer_data.loc[layer_data['cell'] == j].empty:
                layer_data.loc[(layer_data['cell'] == j)].to_csv(f'{write_path}\cell{j}.csv')